# Odoo Finance Suite (`odoo-finance`)

Repositori modul custom Odoo untuk kebutuhan akuntansi, perpajakan, dan operasional bisnis Indonesia.

## 📦 Daftar Modul

| Nama Modul | Deskripsi | Status |
| :--- | :--- | :---: |
| **`sample_app`** | Starter module template Odoo (Task & MVC flow). | ✅ Ready |
| **`l10n_id_coretax_taxation`** | Kepatuhan Pajak Indonesia (PPh 21/22/23/4(2)/Final UMKM PP 20/2026, NITKU & Coretax Export). | 🚧 In Progress |
| **`marketplace_settlement_sync`** | Auto-Parser Excel settlement Shopee, TikTok Shop, Tokopedia ke jurnal Odoo. | ⏳ Planned |
| **`fnb_hpp_calculator`** | Kalkulator HPP & Manajemen Resep Ringan tanpa manufaktur MRP kaku. | ⏳ Planned |
| **`account_stamp_signature`** | Auto-overlay stempel transparan pada tanda tangan digital PDF Invoice/PO. | ⏳ Planned |
| **`financial_health_dashboard`** | Dashboard interaktif rasio likuiditas, solvabilitas, dan margin bisnis. | ⏳ Planned |

---

## 🚀 Panduan Instalasi
1. Clone repositori ini ke folder addons Odoo Anda:
   ```bash
   git clone <repo-url> odoo-finance
   ```
2. Tambahkan path folder ini ke konfigurasi `odoo.conf` pada opsi `addons_path`:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo-finance
   ```
3. Restart server Odoo, aktifkan Developer Mode, lalu lakukan **Update Apps List** pada menu Apps.
