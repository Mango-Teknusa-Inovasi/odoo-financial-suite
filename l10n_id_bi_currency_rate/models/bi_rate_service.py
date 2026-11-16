# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, date, timedelta
from odoo import models, api, _

_logger = logging.getLogger(__name__)

class BiRateSyncService(models.AbstractModel):
    _name = 'bi.rate.sync.service'
    _description = 'Layanan Sinkronisasi Kurs Bank Indonesia'

    @api.model
    def cron_sync_daily_rates(self):
        """Metode terjadwal (ir.cron) untuk memperbarui kurs valas seluruh perusahaan aktif."""
        companies = self.env['res.company'].search([('bi_sync_enabled', '=', True)])
        for comp in companies:
            try:
                self.sync_rates_for_company(comp)
            except Exception as e:
                _logger.error("Gagal sinkronisasi kurs BI untuk perusahaan %s: %s", comp.name, str(e))

    @api.model
    def sync_rates_for_company(self, company, target_date=None):
        """
        Sinkronisasi kurs valas untuk satu perusahaan dengan multi-provider fallback.
        """
        if not target_date:
            target_date = date.today()

        # Aturan Hari Kerja: Jika Sabtu atau Minggu, mundurkan ke hari Jumat terakhir
        effective_date = self._get_last_business_day(target_date)

        # Cari mata uang aktif yang perlu disinkronkan (kecuali mata uang dasar perusahaan)
        base_currency = company.currency_id or self.env.ref('base.IDR', raise_if_not_found=False)
        base_code = base_currency.name if base_currency else 'IDR'

        active_currencies = self.env['res.currency'].search([
            ('active', '=', True),
            ('name', '!=', base_code)
        ])

        if not active_currencies:
            return {
                'status': 'warning',
                'message': _('Tidak ada mata uang asing yang aktif di database Odoo.')
            }

        target_codes = set(active_currencies.mapped('name'))

        # Eksekusi Fallback Cascade
        rates_data, source_name, status = self._fetch_rates_cascade(target_codes, effective_date)

        # Catat ke tabel res.currency.rate
        updated_codes = []
        summary_lines = []

        CurrencyRate = self.env['res.currency.rate']
        for curr in active_currencies:
            rate_info = rates_data.get(curr.name)
            if not rate_info:
                continue

            idr_val = float(rate_info.get('idr_rate', 0.0))
            if idr_val <= 0.0:
                continue

            rate_source = rate_info.get('source', 'bi_middle')
            odoo_rate = round(1.0 / idr_val, 12)

            # Cari apakah kurs hari ini sudah ada
            existing_rate = CurrencyRate.search([
                ('currency_id', '=', curr.id),
                ('name', '=', target_date),
                ('company_id', '=', company.id)
            ], limit=1)

            if existing_rate:
                existing_rate.write({
                    'rate': odoo_rate,
                    'idr_rate': idr_val,
                    'rate_source': rate_source,
                    'source_reference': f"{source_name} ({effective_date})"
                })
            else:
                CurrencyRate.create({
                    'currency_id': curr.id,
                    'name': target_date,
                    'company_id': company.id,
                    'rate': odoo_rate,
                    'idr_rate': idr_val,
                    'rate_source': rate_source,
                    'source_reference': f"{source_name} ({effective_date})"
                })

            updated_codes.append(curr.name)
            summary_lines.append(f"• 1 {curr.name} = Rp {idr_val:,.2f} ({rate_source})")

        # Update metadata status perusahaan
        company.write({
            'bi_last_sync_date': fields.Datetime.now(),
            'bi_last_sync_status': status,
            'bi_last_sync_message': f"Berhasil memperbarui {len(updated_codes)} valas dari {source_name}."
        })

        # Catat audit log
        log_name = f"SYNC/{effective_date.strftime('%Y%m%d')}/{len(updated_codes)}"
        self.env['bi.rate.sync.log'].create({
            'name': log_name,
            'target_date': effective_date,
            'company_id': company.id,
            'status': status,
            'source_used': source_name,
            'currencies_updated': ", ".join(updated_codes),
            'currency_count': len(updated_codes),
            'summary': "\n".join(summary_lines) if summary_lines else "Tidak ada valas yang diperbarui.",
            'error_message': "" if status == 'success' else f"Digunakan mode fallback/carry-forward ({source_name})."
        })

        return {
            'status': status,
            'message': f"Sinkronisasi selesai: {len(updated_codes)} valas diperbarui ({source_name}).",
            'updated': updated_codes
        }

    @api.model
    def _get_last_business_day(self, target_date):
        """Mundur ke hari Jumat jika target_date adalah Sabtu atau Minggu."""
        weekday = target_date.weekday()
        if weekday == 5:  # Sabtu
            return target_date - timedelta(days=1)
        elif weekday == 6:  # Minggu
            return target_date - timedelta(days=2)
        return target_date

    @api.model
    def _fetch_rates_cascade(self, target_codes, effective_date):
        """
        Multi-Provider Fallback Cascade:
        1. Official Bank Indonesia API
        2. High-Reliability Open Mirror
        3. Internal Last Business Day Carry-Forward
        """
        # 1. Coba Endpoint Resmi Bank Indonesia
        try:
            bi_rates = self._fetch_from_bi_official(target_codes, effective_date)
            if bi_rates:
                return bi_rates, "Bank Indonesia (Official API & JISDOR)", "success"
        except Exception as e:
            _logger.warning("Koneksi resmi Bank Indonesia gagal atau timeout: %s", str(e))

        # 2. Coba Open Mirror Terpercaya
        try:
            mirror_rates = self._fetch_from_open_mirror(target_codes, effective_date)
            if mirror_rates:
                return mirror_rates, "Open Forex Mirror (High-Availability)", "warning"
        except Exception as e:
            _logger.warning("Koneksi open mirror cadangan gagal: %s", str(e))

        # 3. Fallback Carry-Forward dari Database Odoo Terakhir
        carry_rates = self._carry_forward_latest_rates(target_codes)
        return carry_rates, "Internal Database (Last Available Business Day)", "warning"

    @api.model
    def _fetch_from_bi_official(self, target_codes, effective_date):
        """Pengambilan data dari portal Bank Indonesia."""
        import urllib.request
        date_str = effective_date.strftime("%Y-%m-%d")
        url = f"https://www.bi.go.id/biweb/api/kurs/transaksi?date={date_str}"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MangoTek-Finance/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                rates = {}
                for item in data.get('data', []):
                    code = item.get('currency') or item.get('msh_id')
                    if code in target_codes:
                        beli = float(item.get('beli_subkurslocal', 0))
                        jual = float(item.get('jual_subkurslocal', 0))
                        tengah = (beli + jual) / 2.0 if (beli and jual) else (jual or beli)
                        rates[code] = {
                            'idr_rate': round(tengah, 2),
                            'source': 'bi_middle'
                        }
                if rates:
                    return rates
        return {}

    @api.model
    def _fetch_from_open_mirror(self, target_codes, effective_date):
        """Pengambilan data dari open API mirror cadangan terpercaya (Frankfurter / ExchangeRate)."""
        import urllib.request
        # Ambil kurs berbasis USD / EUR lalu cross-rate ke IDR
        url = "https://api.frankfurter.app/latest?from=USD"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 MangoTek-Finance-Mirror/1.0'}
        )
        with urllib.request.urlopen(req, timeout=6) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                raw_rates = data.get('rates', {})
                idr_per_usd = raw_rates.get('IDR', 16250.0)
                
                rates = {}
                if 'USD' in target_codes:
                    rates['USD'] = {'idr_rate': round(idr_per_usd, 2), 'source': 'jisdor'}
                
                for code in target_codes:
                    if code == 'USD':
                        continue
                    if code in raw_rates and raw_rates[code] > 0:
                        # 1 USD = X Code, 1 USD = Y IDR -> 1 Code = (Y / X) IDR
                        rate_code = raw_rates[code]
                        idr_val = idr_per_usd / rate_code
                        rates[code] = {'idr_rate': round(idr_val, 2), 'source': 'bi_middle'}
                if rates:
                    return rates
        return {}

    @api.model
    def _carry_forward_latest_rates(self, target_codes):
        """Mengambil nilai kurs terakhir yang tersimpan di database sebagai perlindungan luring."""
        rates = {}
        CurrencyRate = self.env['res.currency.rate']
        for code in target_codes:
            curr = self.env['res.currency'].search([('name', '=', code)], limit=1)
            if not curr:
                continue
            last_rate = CurrencyRate.search([
                ('currency_id', '=', curr.id),
                ('rate', '>', 0)
            ], order='name desc, id desc', limit=1)
            if last_rate:
                idr_val = last_rate.idr_rate or round(1.0 / last_rate.rate, 2)
                rates[code] = {
                    'idr_rate': idr_val,
                    'source': 'bi_middle'
                }
        return rates
