# -*- coding: utf-8 -*-
import io
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PosThermalTemplate(models.Model):
    _name = 'pos.thermal.template'
    _description = 'Template Struk Kasir Thermal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'is_default desc, id desc'

    name = fields.Char(
        string="Nama Template",
        required=True,
        tracking=True,
        help="Nama konfigurasi struk (misal: Struk Kasir 58mm Portable)."
    )
    code = fields.Char(
        string="Kode Template",
        required=True,
        copy=False,
        default="RCP/001",
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string="Perusahaan",
        required=True,
        default=lambda self: self.env.company
    )
    is_default = fields.Boolean(
        string="Template Default",
        default=False,
        tracking=True,
        help="Gunakan template ini secara otomatis jika tidak ditentukan pada transaksi."
    )

    # Paper & Grid Settings
    paper_width = fields.Selection([
        ('58mm', '58 mm (32 Karakter / Mini Bluetooth Portable)'),
        ('80mm', '80 mm (48 Karakter / Desktop Counter Printer)')
    ], string="Lebar Kertas Thermal", default='58mm', required=True, tracking=True)

    font_family = fields.Selection([
        ('monospace', 'Font A - Monospace Standar (ESC/POS 12x24)'),
        ('compact', 'Font B - Kondensasi / Hemat Kertas (ESC/POS 9x17)')
    ], string="Karakter Font", default='monospace', required=True)

    char_per_line = fields.Integer(
        string="Karakter Per Baris",
        compute='_compute_char_per_line',
        store=True
    )

    # Header & Store Info
    show_logo = fields.Boolean(string="Tampilkan Logo Toko", default=True)
    logo_image = fields.Binary(string="Unggah Logo Toko")
    logo_dithered = fields.Binary(
        string="Bitmap Monokrom 1-Bit",
        compute='_compute_logo_dithered',
        store=True,
        help="Hasil konversi otomatis 1-bit hitam-putih tanpa gradasi abu-abu agar tajam di printer thermal."
    )
    header_title = fields.Char(
        string="Nama Toko / Merchant",
        default="MANGO STORE INDONESIA",
        tracking=True
    )
    store_address = fields.Text(
        string="Alamat Lengkap Toko",
        default="Jl. Senopati No. 45, Kebayoran Baru, Jakarta Selatan"
    )
    store_phone = fields.Char(
        string="No. Telepon / WhatsApp CS",
        default="0812-3456-7890"
    )
    store_npwp = fields.Char(
        string="NPWP / NITKU Toko",
        default="01.234.567.8-012.000"
    )

    # Metadata Visibility
    show_order_number = fields.Boolean(string="Tampilkan No. Struk", default=True)
    show_cashier_name = fields.Boolean(string="Tampilkan Nama Kasir", default=True)
    show_customer_name = fields.Boolean(string="Tampilkan Nama Pelanggan", default=True)
    show_timestamp = fields.Boolean(string="Tampilkan Tanggal & Jam", default=True)

    # Order Lines Formatting
    line_style = fields.Selection([
        ('adaptive_dual', 'Mode 2 Baris: Nama Produk Penuh lalu Qty x Harga (Anti-Terpotong)'),
        ('single_line', 'Mode 1 Baris: Nama Produk Sebaris dengan Total')
    ], string="Format Baris Produk", default='adaptive_dual', required=True)

    show_discount = fields.Boolean(string="Tampilkan Rincian Diskon Item", default=True)
    show_tax_detail = fields.Boolean(string="Tampilkan Rincian PPN / Pajak", default=True)

    # QRIS & Barcode Settings
    show_qris = fields.Boolean(string="Tampilkan QR Code Pembayaran (QRIS)", default=True)
    qris_image_source = fields.Selection([
        ('auto_qbiz', 'Otomatis dari Modul QBiz Dynamic QRIS (account_qris_qbiz)'),
        ('custom_qr', 'QR Code Statis / URL Kustom Toko')
    ], string="Sumber Gambar QRIS", default='auto_qbiz')
    custom_qr_payload = fields.Char(
        string="Payload QR Statis",
        default="https://mangotek.id"
    )

    # Footer & Social Engagement
    footer_message = fields.Text(
        string="Pesan Terima Kasih",
        default="Terima kasih atas kunjungan Anda!\nBarang yang sudah dibeli tidak dapat ditukar."
    )
    wifi_ssid = fields.Char(string="Nama WiFi Toko", default="MangoGuest")
    wifi_password = fields.Char(string="Password WiFi", default="kopiindonesia")
    instagram_handle = fields.Char(string="Instagram Toko", default="@mangostore.id")
    tiktok_handle = fields.Char(string="TikTok Toko", default="@mangostore")
    return_policy = fields.Text(string="Kebijakan Garansi / Retur")
    cut_paper = fields.Boolean(string="Potong Kertas Otomatis (Auto-Cut)", default=True)

    # Live Preview HTML
    preview_html = fields.Html(
        string="Simulasi Visual Kertas Thermal",
        compute='_compute_preview_html',
        sanitize=False
    )

    @api.depends('paper_width')
    def _compute_char_per_line(self):
        for rec in self:
            rec.char_per_line = 32 if rec.paper_width == '58mm' else 48

    @api.depends('logo_image', 'paper_width')
    def _compute_logo_dithered(self):
        """Konversi logo berwarna ke bitmap 1-bit monokrom beresolusi tinggi."""
        for rec in self:
            if not rec.logo_image:
                rec.logo_dithered = False
                continue
            try:
                from PIL import Image
                max_w = 384 if rec.paper_width == '58mm' else 576
                raw_data = base64.b64decode(rec.logo_image)
                img = Image.open(io.BytesIO(raw_data)).convert('RGB')
                
                # Aspect ratio resize
                w_percent = (max_w / float(img.size[0]))
                if w_percent < 1.0:
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img = img.resize((max_w, h_size), Image.Resampling.LANCZOS)
                
                # 1-bit Floyd-Steinberg dithering
                dithered = img.convert('1')
                out_io = io.BytesIO()
                dithered.save(out_io, format='PNG')
                rec.logo_dithered = base64.b64encode(out_io.getvalue())
            except Exception:
                rec.logo_dithered = rec.logo_image

    @api.depends(
        'paper_width', 'header_title', 'store_address', 'store_phone', 'store_npwp',
        'line_style', 'show_discount', 'show_tax_detail', 'show_qris',
        'footer_message', 'wifi_ssid', 'wifi_password', 'instagram_handle', 'tiktok_handle'
    )
    def _compute_preview_html(self):
        """Bangun simulasi visual gulungan kertas thermal monokrom real-time."""
        for rec in self:
            width_px = 280 if rec.paper_width == '58mm' else 380
            cols = 32 if rec.paper_width == '58mm' else 48
            sep_line = '-' * cols
            double_sep = '=' * cols

            # Mock receipt items
            items_html = ""
            if rec.line_style == 'adaptive_dual':
                items_html += f"""
                <div style="margin-bottom: 4px;">
                    <div>Kopi Susu Aren Spesial</div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>&nbsp;&nbsp;2 x 18.000</span>
                        <span>36.000</span>
                    </div>
                </div>
                <div style="margin-bottom: 4px;">
                    <div>Roti Bakar Coklat Keju</div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>&nbsp;&nbsp;1 x 25.000</span>
                        <span>25.000</span>
                    </div>
                </div>
                """
            else:
                items_html += """
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 60%;">2x Kopi Susu Aren</span>
                    <span>36.000</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                    <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 60%;">1x Roti Bakar Coklat</span>
                    <span>25.000</span>
                </div>
                """

            wifi_block = ""
            if rec.wifi_ssid:
                wifi_block = f"""<div>WiFi: <strong>{rec.wifi_ssid}</strong> ({rec.wifi_password or '-'})</div>"""

            social_block = ""
            if rec.instagram_handle or rec.tiktok_handle:
                handles = []
                if rec.instagram_handle:
                    handles.append(f"IG: {rec.instagram_handle}")
                if rec.tiktok_handle:
                    handles.append(f"TikTok: {rec.tiktok_handle}")
                social_block = f"""<div>{' · '.join(handles)}</div>"""

            qris_block = ""
            if rec.show_qris:
                qris_block = f"""
                <div style="text-align: center; margin: 8px 0;">
                    <div style="display: inline-block; padding: 4px; border: 2px solid #000; background: #FFF;">
                        <div style="width: 80px; height: 80px; background: repeating-linear-gradient(45deg, #000, #000 4px, #fff 4px, #fff 8px); margin: 0 auto;"></div>
                    </div>
                    <div style="font-size: 10px; margin-top: 2px;">SCAN QRIS UNTUK BAYAR</div>
                </div>
                """

            html = f"""
            <div style="width: {width_px}px; margin: 0 auto; background: #FFFFF8; color: #111; font-family: 'Courier New', Courier, monospace; font-size: 11px; line-height: 1.35; padding: 16px 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border-radius: 4px; border-top: 5px dashed #CBD5E1; border-bottom: 5px dashed #CBD5E1;">
                <div style="text-align: center; margin-bottom: 8px;">
                    <div style="font-weight: bold; font-size: 13px; text-transform: uppercase;">{rec.header_title or 'NAMA TOKO'}</div>
                    <div style="font-size: 10px;">{rec.store_address or ''}</div>
                    <div style="font-size: 10px;">Telp: {rec.store_phone or '-'}</div>
                    <div style="font-size: 9px; color: #444;">NPWP: {rec.store_npwp or '-'}</div>
                </div>
                
                <div style="text-align: center; letter-spacing: -1px; margin: 3px 0; color: #666;">{sep_line}</div>
                
                <div style="font-size: 10px; margin-bottom: 4px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>No: POS/2026/0042</span>
                        <span>17/11/2026 10:15</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Kasir: Budi Santoso</span>
                        <span>Pelanggan Umum</span>
                    </div>
                </div>
                
                <div style="text-align: center; letter-spacing: -1px; margin: 3px 0; color: #000;">{double_sep}</div>
                
                {items_html}
                
                <div style="text-align: center; letter-spacing: -1px; margin: 3px 0; color: #666;">{sep_line}</div>
                
                <div style="font-size: 11px;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Subtotal</span>
                        <span>61.000</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>PPN 12%</span>
                        <span>7.320</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; margin-top: 2px;">
                        <span>TOTAL</span>
                        <span>68.320</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 3px;">
                        <span>TUNAI</span>
                        <span>70.000</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>KEMBALI</span>
                        <span>1.680</span>
                    </div>
                </div>
                
                {qris_block}
                
                <div style="text-align: center; letter-spacing: -1px; margin: 4px 0; color: #666;">{sep_line}</div>
                
                <div style="text-align: center; font-size: 10px;">
                    <div style="white-space: pre-line; margin-bottom: 4px;">{rec.footer_message or ''}</div>
                    {wifi_block}
                    {social_block}
                </div>
            </div>
            """
            rec.preview_html = html

    def action_set_as_default(self):
        """Tetapkan template ini sebagai default dan nonaktifkan template lainnya pada perusahaan."""
        self.ensure_one()
        self.search([
            ('company_id', '=', self.company_id.id),
            ('id', '!=', self.id)
        ]).write({'is_default': False})
        self.is_default = True

    def action_print_sample(self):
        """Cetak struk sampel thermal untuk uji coba printer."""
        self.ensure_one()
        report_xmlid = 'pos_thermal_receipt_designer.action_report_sample_thermal_58mm' if self.paper_width == '58mm' else 'pos_thermal_receipt_designer.action_report_sample_thermal_80mm'
        return self.env.ref(report_xmlid).report_action(self)

    def generate_escpos_bytes(self, order_data):
        """
        Pure Python ESC/POS byte sequence generator.
        Mendukung initialize, center, left, bold, double height, dan auto-cut.
        """
        cols = self.char_per_line or 32
        ESC = b'\x1b'
        GS = b'\x1d'

        buf = bytearray()
        # Initialize printer
        buf.extend(ESC + b'@')

        # Header Centered
        buf.extend(ESC + b'a\x01')  # Align Center
        buf.extend(ESC + b'E\x01')  # Bold On
        buf.extend(GS + b'!\x11')   # Double height & width
        buf.extend((self.header_title or '').encode('latin1', 'replace') + b'\n')
        buf.extend(GS + b'!\x00')   # Normal size
        buf.extend(ESC + b'E\x00')  # Bold Off

        if self.store_address:
            buf.extend((self.store_address).encode('latin1', 'replace') + b'\n')
        if self.store_phone:
            buf.extend((f"Telp: {self.store_phone}").encode('latin1', 'replace') + b'\n')
        if self.store_npwp:
            buf.extend((f"NPWP: {self.store_npwp}").encode('latin1', 'replace') + b'\n')

        # Divider
        buf.extend(ESC + b'a\x00')  # Align Left
        buf.extend((b'-' * cols) + b'\n')

        # Items
        items = order_data.get('items', [])
        for it in items:
            name = it.get('name', 'Item')
            qty = it.get('qty', 1)
            price = it.get('price', 0.0)
            total = it.get('total', 0.0)

            if self.line_style == 'adaptive_dual':
                buf.extend(name[:cols].encode('latin1', 'replace') + b'\n')
                left_str = f"  {qty} x {price:,.0f}"
                right_str = f"{total:,.0f}"
                space = cols - len(left_str) - len(right_str)
                line = left_str + (' ' * max(space, 1)) + right_str
                buf.extend(line.encode('latin1', 'replace') + b'\n')
            else:
                left_str = f"{qty}x {name[:cols-15]}"
                right_str = f"{total:,.0f}"
                space = cols - len(left_str) - len(right_str)
                line = left_str + (' ' * max(space, 1)) + right_str
                buf.extend(line.encode('latin1', 'replace') + b'\n')

        # Totals
        buf.extend((b'-' * cols) + b'\n')
        total_str = f"TOTAL: {order_data.get('amount_total', 0.0):,.0f}"
        buf.extend(ESC + b'a\x02')  # Align Right
        buf.extend(ESC + b'E\x01')  # Bold On
        buf.extend(total_str.encode('latin1', 'replace') + b'\n')
        buf.extend(ESC + b'E\x00')  # Bold Off

        # Footer
        buf.extend(ESC + b'a\x01')  # Align Center
        buf.extend((b'-' * cols) + b'\n')
        if self.footer_message:
            buf.extend(self.footer_message.encode('latin1', 'replace') + b'\n')
        if self.wifi_ssid:
            buf.extend(f"WiFi: {self.wifi_ssid} ({self.wifi_password})\n".encode('latin1', 'replace'))

        # Line feeds and Auto Cut
        buf.extend(b'\n\n\n')
        if self.cut_paper:
            buf.extend(GS + b'V\x42\x00')  # GS V 66 0

        return bytes(buf)
