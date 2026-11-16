<div align="center">

![MangoTek Financial Suite Banner](assets/banner.png)

# 📸 MangoTek Financial Suite — Visual Showcase & Live Verification Gallery
### *Enterprise Indonesian Tax Localization, Marketplace Settlement, Recipe Costing & CFO Diagnostics for Odoo 18.0, 19.0 & 20.0*

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](LICENSE)
[![Price: 100% Free](https://img.shields.io/badge/Price-100%25%20Free-brightgreen.svg)](#)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0%20%7C%2019.0%20%7C%2020.0-purple.svg)](https://www.odoo.com/)
[![App Store Ready](https://img.shields.io/badge/Odoo%20Apps%20Store-5%2F5%20Score%20Ready-brightgreen.svg)](#)

</div>

---

## 🧭 Suite Overview & Application Launcher

All 5 core modules of the **MangoTek Financial Suite** are natively integrated into the standard Odoo web client. Each module possesses custom geometric vector iconography conforming to Odoo's design tokens and is instantly accessible from the 9-dots App Drawer.

<div align="center">

![Odoo App Launcher Suite Complete](assets/screenshots/01_app_launcher_suite.png)
*Figure 1: Odoo 18.0 App Drawer featuring all 5 MangoTek Financial Suite applications running live.*

</div>

---

## 🏛️ Module 1: Indonesian Tax Coretax (`l10n_id_coretax_taxation`)
> **Directory:** `l10n_id_coretax_taxation` | **Odoo Version:** `18.0.1.0.0` | **License:** `LGPL-3.0`

### Statutory Capabilities:
- **DJP Coretax 2026 & e-Faktur 4.0 Readiness:** Automatic calculation of statutory PPN 12% (UU HPP) and DPP Nilai Lain.
- **Automated NSFP Pool Allocation:** Real-time sequential Nomor Seri Faktur Pajak pool distribution upon posting customer invoices.
- **PMK 112/PMK.03/2022 Validation:** Strict 16-digit NIK/NPWP16 and 22-digit NITKU validation on partner master data.
- **Comprehensive Withholding Taxes:** PPh 21, 22, 23, 4(2), and PPh Final UMKM 0.5% (Government Regulation PP 20/2026).
- **Statutory Batch Export:** 1-click wizard generating DJP-compliant `FK` (Faktur Keluaran) and `OF` (Objek Faktur) CSV exports.

<div align="center">

![Coretax Invoice & Tax Breakdown](assets/screenshots/02_coretax_invoice_tax.png)
*Figure 2: Customer Invoice with automated NSFP serial allocation, statutory PPN 12%, and withholding tax line.*

</div>

---

## 🛒 Module 2: Multichannel Marketplace Settlement Sync (`marketplace_settlement_sync`)
> **Directory:** `marketplace_settlement_sync` | **Odoo Version:** `18.0.1.0.0` | **License:** `LGPL-3.0`

### Operational Capabilities:
- **Direct Statement Parser:** Ingests raw export statements (.xlsx and .csv) from Shopee Seller Centre, Tokopedia Seller, and TikTok Shop Seller Center.
- **Intelligent Split-Accounting:** Automatically separates Gross Merchandise Value (GMV), Platform Commissions, Shipping Deductions, and Net Escrow Payouts into balanced double-entry journal lines.
- **Batch Reconciliation Preview:** Full order-level line item drilldown with one-click posting to General Ledger.

<div align="center">

![Marketplace Settlement Ingestion](assets/screenshots/03_marketplace_settlement_batch.png)
*Figure 3: Marketplace settlement batch showing automated split-accounting between Gross Revenue, Platform Deductions, and Escrow Payouts.*

</div>

---

## 🍽️ Module 3: F&B Recipe HPP & Menu Costing (`fnb_hpp_calculator`)
> **Directory:** `fnb_hpp_calculator` | **Odoo Version:** `18.0.1.0.0` | **License:** `LGPL-3.0`

### Operational Capabilities:
- **Agile Recipe Costing:** Calculates portion HPP directly from raw ingredient purchasing units without heavy MRP overhead.
- **Shrinkage & Waste Factor (%):** Adjusts costs dynamically for trimming, boiling loss, and preparation wastage.
- **Packaging Layer:** Incorporates cups, lids, straws, and takeaway packaging into the true cost per portion.
- **Margin Simulator & POS Sync:** Interactive pricing wizard that pushes updated standard costs and retail prices directly to Odoo Point of Sale catalog products.

<div align="center">

![F&B Recipe Costing Kanban](assets/screenshots/04_fnb_recipe_costing_kanban.png)
*Figure 4: Recipe Costing Kanban dashboard showing real-time portion HPP, target retail prices, and color-coded margin health indicators.*

</div>

---

## 🖋️ Module 4: Stamp & Peruri e-Meterai Gateway (`account_stamp_signature`)
> **Directory:** `account_stamp_signature` | **Odoo Version:** `18.0.1.0.0` | **License:** `LGPL-3.0`

### Statutory & Legal Branding Capabilities:
- **Engine A (100% Free & Offline Wet Seal):** Transparent PNG corporate wet stamp overlay rendered with dynamic $-6^\circ$ tilt and $82\%$ opacity overlapping the authorized digital signature on standard Odoo QWeb PDF invoices.
- **Engine B (Statutory Peruri e-Meterai):** Automatic threshold detection under Indonesian Law **UU No. 10/2020** flagging invoices $\ge \text{Rp } 5.000.000$ for Bea Meterai duty (Rp 10.000).
- **Driver Provider Architecture:** Pluggable connectors for Peruri Digital Security (PDS), Mekari Sign, PrivyID, and built-in Local Sandbox Mock Simulator (100 test stamps).
- **Audit Verifiability:** Generates official 22-digit Peruri Serial Numbers (`SN-2026-XXXXXXXXXXXXXX`) and public QR verification barcodes embedded into QWeb invoice reports.

<div align="center">

![Invoice Stamped with Peruri e-Meterai](assets/screenshots/05_invoice_emeterai_stamped.png)
*Figure 5: Customer invoice `INV/2026/00002` stamped with Peruri Serial Number and legal verification QR code.*

<br/>

![e-Meterai Provider Configuration](assets/screenshots/06_emeterai_provider_config.png)
*Figure 6: Pluggable e-Meterai provider configuration dashboard supporting PDS, Mekari Sign, PrivyID, and Local Sandbox.*

<br/>

![Rendered Stamped Invoice PDF](assets/screenshots/07_stamped_invoice_pdf_preview.png)
*Figure 7: High-resolution QWeb PDF invoice printout displaying the -6° tilted corporate wet seal and Peruri e-Meterai rosette.*

</div>

---

## 📈 Module 5: Executive Financial Health KPI Dashboard (`financial_health_dashboard`)
> **Directory:** `financial_health_dashboard` | **Odoo Version:** `18.0.1.0.0` | **License:** `LGPL-3.0`

### Executive Advisory & Ratio Analysis:
- **Automated Ratio Calculations (from live GL lines):**
  - **Liquidity:** Current Ratio (**2.08x** - Optimal), Quick Ratio (**1.93x** - Optimal), Cash Ratio (**0.00x** - Warning).
  - **Solvency:** Debt-to-Equity / DER (**0.93x** - Conservative), Debt-to-Asset / DAR (**0.48x** - Moderate).
  - **Profitability:** Gross Profit Margin (**52.0%** - Strong), Net Profit Margin (**51.7%** - Highly Profitable).
  - **Working Capital:** Net Working Capital computation (**Rp 66.950.500,00** surplus).
  - **Composite Health Score:** **96 / 100** (*Excellent*).
- **Educational Traffic-Light System:** Instant visual recognition across 🟢 Optimal, 🟡 Moderate, and 🔴 Critical levels.
- **Automated Plain-Language Advisory Diagnostic:** Synthesizes strengths and flags potential cash flow risks (e.g., high AR balance requiring accelerated debt collection).
- **1-Click Drilldown:** Direct jump buttons into Trade Receivables, Payables, and General Ledger.

<div align="center">

![Financial Health Scorecard Kanban](assets/screenshots/08_financial_health_scorecard.png)
*Figure 8: Financial Health Scorecard Kanban showing 96/100 score, Current Ratio 2.08x, DER 0.93x, and Net Margin 51.7%.*

<br/>

![Financial Health Form & Executive Advisory](assets/screenshots/09_financial_health_advisory_form.png)
*Figure 9: Detailed multi-tab ratio analysis view with Balance Sheet breakdown and automated executive narrative synthesis.*

</div>

---

## 📋 Odoo Apps Store Vendor Guidelines Compliance

All modules within this repository have been audited against the official **Odoo Apps Vendor Guidelines**:

| Guideline Requirement | Implementation Standard | Compliance Status |
|:---|:---|:---:|
| **App Name (`name`)** | Maximum 25 characters, explicit, zero company names, zero adjectives | **✅ 100% PASS** |
| **Semantic Version (`version`)** | Follows `<odoo_version>.1.0.0` (e.g., `18.0.1.0.0`, `19.0.1.0.0`, `20.0.1.0.0`) | **✅ 100% PASS** |
| **Open-Source License (`license`)** | Officially licensed under `LGPL-3` without proprietary locks | **✅ 100% PASS** |
| **Dependencies (`depends`)** | Strictly lists valid standard Odoo core modules (`base`, `account`, `product`, `mail`) | **✅ 100% PASS** |
| **Icon Quality (`icon.png`)** | Custom geometric vector icon (100x100 PNG) in `static/description/` | **✅ 100% PASS** |
| **Cover Thumbnail (`images`)** | Dedicated 1200x630 `static/description/banner.png` declared in `images` | **✅ 100% PASS** |
| **HTML Description (`index.html`)** | 100% English description with Bootstrap 4 classes and zero forbidden external links | **✅ 100% PASS** |
| **Price & Currency (`price`)** | Free tier (`0.0 EUR`), zero activation keys, zero vendor lock-in | **✅ 100% PASS** |
| **App Store Score Potential** | Fulfills all 5 scoring criteria for maximum **5 / 5** store ranking | **✅ 100% PASS** |

---

<div align="center">

**Developed with ❤️ by [Mango Teknusa Inovasi](https://github.com/Mango-Teknusa-Inovasi)**  
*For questions, enterprise support, or localization requests, contact: [billing@ppti.me](mailto:billing@ppti.me)*

</div>
