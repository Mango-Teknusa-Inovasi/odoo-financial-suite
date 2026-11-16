# Changelog

All notable changes to the **MangoTek Financial Suite** are documented in this file.

The format follows standard semantic versioning practices (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Planned (Phase 12 Horizon)
- **Phase 12: `account_simple_budgeting`:** Monthly revenue target and expense limit monitoring with traffic-light visual progress gauges.

---

## [1.3.0] - 2026-11-17

### Added (Phase 11: Bank Indonesia Official Currency Rate Auto-Sync)
- **Core Module `l10n_id_bi_currency_rate`:** Enterprise automated currency exchange rate synchronization engine fetching official Bank Indonesia rates (JISDOR for USD & Kurs Transaksi BI for other foreign currencies) and Kemenkeu KMK weekly fiscal tax rates.
- **Dual-Stream Rate Synchronization:** Automated ingestion separating commercial accounting rates (JISDOR/Kurs Tengah) from statutory tax rates (KMK) used for PPN 12% and e-Faktur compliance.
- **3-Tier Multi-Provider Fallback Cascade:**
  - *Tier 1 (Official BI API & Feeds):* Direct ingestion from Bank Indonesia web endpoints with 5s network timeout tolerance.
  - *Tier 2 (High-Availability Open Mirror):* Automatic failover to reliable open exchange rate mirrors if government portals experience maintenance or timeouts.
  - *Tier 3 (Last Business Day Carry-Forward):* Internal database fallback carrying forward the latest active Friday business day rates during weekends or public holidays.
- **Active Currencies Filter:** Selectively updates only foreign currencies actively configured in the company database (e.g. USD, EUR, SGD, JPY, CNY, MYR), avoiding database bloat.
- **Human-Friendly Rupiah Grid (`idr_rate`):** Custom bidirectional monetary field allowing accountants to view and edit rates directly in familiar Rupiah (e.g. Rp 16,250.00) while automatically calculating Odoo's inverted fractional rate ($1/\text{IDR}$).
- **Automated 17:00 WIB Scheduled Cron (`ir.cron`):** Daily background execution scheduled after market close and final JISDOR rate publication, plus 1-click manual trigger button in Invoicing Settings.
- **Audited History Model (`bi.rate.sync.log`):** Multi-company historical audit trail tracking sync timestamps, data provider origin, execution status, and currency rate summaries.

### Added (Phase 10: POS Thermal Receipt Designer & ESC/POS Engine)
- **Core Module `pos_thermal_receipt_designer`:** Enterprise visual thermal receipt designer and dual-engine ESC/POS & QWeb generator supporting 58 mm mini Bluetooth and 80 mm desktop POS continuous rolls.
- **Dual Width Presets & Dynamic Grid:** Native paperformat records for 58 mm (32 characters per line) and 80 mm (48 characters per line) with automated monospace grid computation.
- **Live Sticky WYSIWYG Form Simulation:** Real-time responsive paper roll preview updating instantly upon changing store headers, footers, policies, and item layout styles.
- **1-Bit Floyd-Steinberg Monochrome Dithering:** Automated PIL dithering converting full-color store logos into crisp, high-contrast 1-bit monochrome bitmaps without gray blurriness.
- **Dynamic QRIS Payment Block:** Direct ingestion of QBiz Dynamic QRIS (`account_qris_qbiz`) with CRC16 and unique invoice nominals, plus fallback to custom static QR codes.
- **Adaptive Dual-Line Item Layout:** Eliminates truncation on narrow 58 mm paper by rendering item names on top and quantity x price with right-aligned line totals below.
- **Pure Python ESC/POS Byte Sequence Generator:** Low-level ESC/POS byte generator (`generate_escpos_bytes()`) supporting printer initialize, text alignment, double-height headers, bold totals, line feeds, and automatic paper cutting (`GS V 66 0`).
- **Dual-Channel Invoicing & POS Integration:** Print thermal receipts directly from Customer Invoices (`account.move`) or POS orders with company default template fallback.
- **Social Engagement & Store Amenities:** Form fields for store WiFi SSID & password, Instagram/TikTok handles, return policies, and custom marketing footer slogans.

### Added (Phase 9: Lightweight Project Job Costing)
- **Core Module `account_project_job_costing`:** Agile project cost sheet and profit tracker providing dual-metric financial performance (Accrual P&L vs Real Cashflow) without requiring complex Odoo Analytic Distribution matrices.
- **Dual-Metric Real-Time Financial Engine:**
  - **Metric 1: Accrual P&L (Laba Rugi Akrual):** Invoiced Revenue minus categorized project expenses (Material, Labor, Overhead) computing Net Accrual Profit and Accrual Margin %.
  - **Metric 2: Realized Cash Position (Posisi Kas Nyata):** Real payments collected from customer invoices minus real disbursements to supplier bills, plus visibility on Uncollected AR and Unpaid AP.
- **Multi-Category Budget Tracking & Burn Rate:** Plafon budgets for Materials, Labor/Subcontractors, and Overhead with real-time variance and traffic-light health status (🟢 Sehat, 🟡 Perhatian, 🔴 Over Budget).
- **Zero-Overhead Transaction Ingestion:** 1-click project tagging on Customer Invoices and Vendor Bills with auto-cascading to invoice lines and line-level cost classification.
- **Indonesian Withholding Tax (WHT) Calculator:** Sensitivity modeling for PPh 23 (2.0%) and PPh Final Jasa Konstruksi (PP 9/2021: 1.75%, 2.65%, 4.0%) estimating net cash realization after tax.
- **Smart Closure Guard Wizard (`account.job.close.wizard`):** Audit confirmation modal alerting managers of outstanding client receivables or unpaid vendor bills before closing projects.
- **Executive Reporting & Outputs:**
  - Official printable **QWeb PDF Project Cost Sheet** with dual-metric comparison and dual sign-off blocks.
  - One-click **Excel (.xlsx)** transaction export generator with universal CSV UTF-8 BOM fallback.

### Added (Phase 8: WhatsApp Financial Notifier & Document Dispatcher)
- **Core Module `account_whatsapp_notifier`:** Universal multi-engine WhatsApp notification dispatcher for Invoices, Bills, and Customer Follow-ups supporting self-hosted GOWA (Go WhatsApp Web Multidevice), official Meta Cloud API, and native `wa.me` Click-to-Chat.
- **Unofficial Self-Hosted GOWA Gateway Support:** Seamless compatibility with `aldinokemal/go-whatsapp-web-multidevice` including `POST /send/message` for text and `POST /send/file` multipart form-data upload for direct PDF invoice dispatch with device routing (`X-Device-Id`).
- **Interactive Document Composer Wizard (`account.whatsapp.composer`):** Modal dialog with live template preview, phone editor, instant dispatch, PDF attachment checkbox, and 1-click `wa.me` web/mobile fallback.
- **Indonesian Dynamic Template Engine (`account.whatsapp.template`):** Seeded templates for Faktur Baru, Pengingat Jatuh Tempo, and Konfirmasi Pembayaran with dynamic placeholders (`{{partner_name}}`, `{{invoice_number}}`, `{{amount_total}}`, `{{amount_residual}}`, `{{due_date}}`, `{{company_name}}`, `{{portal_url}}`, `{{qris_note}}`, `{{emeterai_status}}`).
- **Indonesian Phone Normalizer (`res.partner`):** Automatic normalization converting Indonesian numbers (`08xx`, `+62 8xx`, `62-8xx`) to standard international E.164 without plus signs (`628xx`).
- **Companion Interoperability & Zero-Crash Coexistence:** Soft integration with `account_qris_qbiz` (appending QRIS payment instructions) and `account_stamp_signature` (e-Meterai status badge) without declaring hard dependencies.
- **Security & Multi-Company:** Granular access controls (`security/ir.model.access.csv`) and multi-company record rules (`security/whatsapp_security.xml`).
- **Odoo Apps Store Assets:** Complete compliance assets with 100x100 squircle icon, standard 1200x630 banner, and responsive store description page (`static/description/index.html`).

### Quality Verification
- `scripts/validate_apps_store.py`: 88/88 checks passed (Score 5.0 / 5.0 across all 11 modules).
- `tests/run_all_tests.py`: 59/59 tests passed (0 failures, 0 errors).
- Multi-Branch Architecture: Verified and synchronized across `main`, `18.0`, `19.0`, and `20.0`.

---

## [1.2.0] - 2026-11-17

### Added (Phase 7: Opening Balance Setup Wizard)
- **Core Module `account_opening_balance_wizard`:** Complete single-window financial balance setup wizard for Indonesian businesses migrating from legacy accounting systems (Accurate, Zahir, Jurnal, SAP, or spreadsheets).
- **Live Dynamic Balance Bar:** Real-time computation of Debits, Credits, and Net Equity Difference directly within the single-window form with color-coded status indicators.
- **Multi-Sheet Excel Engine:** Pre-formatted XLSX export and import template covering Cash/Bank, Customers (AR), Vendors (AP), Inventory, and Fixed Assets with bulk upload parsing.
- **Indonesian Tax Asset Register (`account.simple.asset`):** UU PPh Pasal 11 straight-line monthly depreciation scheduler (Kelompok 1 to 4 and Bangunan Permanen) with automated book value tracking.
- **Zero-Balance Opening Clearing Architecture:** Generates posted customer invoices and vendor bills tagged `is_opening_balance=True` counterbalanced by master opening journal lines, maintaining subledger accuracy with zero general ledger double-counting.
- **Security & Multi-Company:** Granular access controls (`security/ir.model.access.csv`) and multi-company record rules (`security/opening_balance_security.xml`).

### Standardized & Verified (Banner Standardization & Visual Governance)
- **Unified Banner Architecture:** Standardized all 7 module banners (`1200x630`) using dark slate gradient (`#0F172A` to `#182036`), ambient radial glow, 140x140 squircle icon container, top open-source badge, Segoe UI typography, and 3 standard pills.
- **Standardized `account_qris_qbiz` Banner:** Corrected design discrepancy in `account_qris_qbiz` banner to match the master design tokens and layout of the other suite modules.
- **Banner Governance (`BRANDKIT.md` & `scripts/generate_module_banners.py`):** Added Section 8 to `BRANDKIT.md` and established an automated master banner generator script so banner and logo architecture rules are permanently preserved.
- **Compliance & Tests:**
  - `scripts/validate_apps_store.py`: 56/56 checks passed (Score 5.0 / 5.0 across all 7 modules).
  - `tests/run_all_tests.py`: 35/35 unit and feature tests passed with 0 failures and 0 errors.
  - Live Docker Verification: Installed, upgraded, and validated end-to-end inside Docker container `odoo18_web`.

---

## [1.1.0] - 2026-11-16

### Added (Phase 6: QBiz Dynamic QRIS Integration)
- **Core Module `account_qris_qbiz`:** Integrated dynamic QRIS generator and automated bank mutation reconciler ported from [ardianryan/qbiz-qrisdinamis](https://github.com/ardianryan/qbiz-qrisdinamis).
- **EMVCo Engine (`models/qris_emvco.py`):** Standalone pure Python TLV parser, dynamic Tag 54 injection, and Bank Indonesia/ASPI compliant CCITT-16 CRC recalculation (polynomial `0x1021`, initial `0xFFFF`).
- **Unique Code Engine:** Automatic 3-digit anti-collision nominal suffix ensuring collision-free matching across concurrent customer payments.
- **Inbound Webhook Controller (`controllers/qris_webhook.py`):** Public JSON endpoint at `/api/v1/webhook/qris` for instant real-time settlement and automated journal entry reconciliation.
- **Invoice & Report Integration (`views/account_move_views.xml`, `views/report_invoice_qris.xml`):** Header actions, dynamic QR canvas preview, tree view status badges, and official PDF invoice QWeb overlay.
- **Master Banner & Assets:** Updated master branding banner (`assets/banner.svg` & `assets/banner.png`) to showcase all 6 active production modules.

---

## [1.0.0] - 2026-11-16

### Standardized & Verified (Odoo Apps Store Vendor Guidelines Alignment)
- **Manifest Versioning:** Standardized all 5 modules to `<odoo_version>.1.0.0` (`18.0.1.0.0`, `19.0.1.0.0`, and `20.0.1.0.0`) in full compliance with Odoo Apps Store major-minor-bugfix semantics.
- **Name Length Compliance:** Audited and verified all app names to remain strictly $\le 25$ characters without company names or promotional adjectives:
  - `Stamp & e-Meterai` (17 chars)
  - `Financial Health KPI` (20 chars)
  - `F&B Recipe HPP` (14 chars)
  - `Indonesian Tax Coretax` (22 chars)
  - `Marketplace Settlement` (22 chars)
- **App Store Scoring Optimization (5/5 Criteria):**
  - **Criterion 1 (Icons):** Verified crisp geometric vector `static/description/icon.png` (100x100 PNG) in every module.
  - **Criterion 2 (Cover Images):** Generated dedicated 1200x630 cover thumbnails (`static/description/banner.png`) and declared `'images'` list in all manifests.
  - **Criterion 3 (License):** Confirmed explicit `LGPL-3` open-source license in every manifest.
  - **Criterion 4 (Clean Score):** Ensured zero error state upon repository scanning.
  - **Criterion 5 (HTML Descriptions):** Provided beautiful `static/description/index.html` pages using Bootstrap 4 classes and English text.
- **Link & Security Sanitization:** Sanitized all links in `static/description/index.html` to strictly utilize approved `mailto:billing@ppti.me` endpoints, eliminating forbidden external redirects.
- **Pricing & Currency Compliance:** Configured `'price': 0.0` and `'currency': 'EUR'` to formally declare free tier status without activation keys or vendor lock-in.
- **Repository Cleanliness:** Purged legacy temporary scaffold `sample_app` from git across all branches.
- **Visual Verification & Gallery:** Created comprehensive visual proof document `SHOWCASE.md` and archived high-resolution live screenshots in `assets/screenshots/`.
- **Enterprise CI/CD & Security Framework:**
  - **CodeQL Security Analysis (`.github/workflows/codeql.yml`):** Automated semantic vulnerability and code quality scanning for Python.
  - **Continuous Integration Pipeline (`.github/workflows/ci.yml`):** Multi-stage workflow covering Flake8 linting, XML view well-formedness, Odoo Apps vendor compliance, and unit tests across Python 3.10, 3.11, and 3.12.
  - **Vendor Guidelines Validator (`scripts/validate_apps_store.py`):** Automated audit engine verifying 40 compliance rules across all 5 manifests.
  - **Automated Unit & Feature Tests (`tests/run_all_tests.py`):** 24 standalone unit tests with built-in Odoo mock framework testing core mathematical, statutory, and accounting logic.
  - **Automated Dependency Auditing (`.github/dependabot.yml`):** Weekly Dependabot vulnerability checks for Actions and dependencies.

---

## [1.5.0] - 2026-11-16

### Added
- **`financial_health_kpi` (Phase 5 Completed):**
  - **Financial Health Model (`financial.health.kpi`):** Automated ratio computation engine pulling live from standard Odoo 18/19/20 General Ledger journal items (`account.move.line`).
  - **Liquidity Diagnostics:** Current Ratio, Quick Ratio (Acid-Test), and Cash Ratio tracking short-term obligation coverage.
  - **Solvency & Capital Structure:** Debt-to-Equity Ratio (DER) and Debt-to-Asset Ratio (DAR) assessing financial leverage risk.
  - **Profitability Metrics:** Gross Profit Margin (GPM %) and Net Profit Margin (NPM %) measuring operational efficiency.
  - **Educational Traffic-Light System:** Visual status badges (🟢 Optimal, 🟡 Moderate, 🔴 Critical) with built-in financial benchmarks.
  - **Automated Executive Advisory Synthesis:** Dynamic plain-language narrative summarizing key strengths and alerting to receivables collection gaps.
  - **Executive Dashboard Kanban & Form Views:** Progress score gauge (0-100), working capital surplus card, and 1-click drilldowns into Trade Receivables, Trade Payables, and General Ledger.
  - **App Launcher Integration:** Dedicated 9-dots App Drawer launcher icon and menu entry under Accounting > Reporting.
  - **Suite Completion:** All 5 core phases of the MangoTek Financial Suite are now fully implemented, verified live in Docker, and published.

---

## [1.4.0] - 2026-11-16

### Added
- **`account_stamp_signature` (Phase 4 Completed):**
  - **Engine A (Free & Offline):** Dynamic transparent PNG wet seal overlay with $-6^\circ$ tilt and $82\%$ opacity over executive digital signature block on standard QWeb PDF invoices.
  - **Company Settings (`res.company`):** Configurable seal image, authorized signature, signatory name, and official designation.
  - **Engine B (Statutory e-Meterai):** Automatic threshold detection under Indonesian law (UU No. 10/2020) for invoices $\ge \text{Rp } 5.000.000$.
  - **Pluggable Gateway Architecture (`emeterai.provider`):** Driver pattern supporting Peruri Digital Security (PDS), Mekari Sign, PrivyID, and built-in Local Sandbox Engine with 100 free test stamps.
  - **Peruri Serial Number & Verification:** Real-time generation of 22-digit Peruri SN and public verification QR code URL.
  - **Statutory QWeb Invoice Badge:** Official bordered rosette badge displaying `BEA METERAI LUNAS Rp 10.000,-`, live QR barcode, and audit reference on `account.report_invoice_document`.
  - **Chatter Audit Trail:** Automatic message posting on invoice confirmation with e-Meterai SN and verification links.
  - **App Launcher Integration:** Dedicated 9-dots App Drawer menu and configuration entry under Accounting > Configuration.
- **Master Branding Refinement:**
  - Restored pristine Mango Gem master logo (circular fruit silhouette with fresh emerald leaf and white M monogram) across all banner and icon assets.
  - Re-rendered master hero banner (`assets/banner.png`, 1200x630) with centered layout and `🟣 Odoo 18.0, 19.0 & 20.0` compatibility chips.

---

## [1.3.0] - 2026-11-16

### Added
- **`fnb_hpp_calculator` (Phase 3 Completed):**
  - Recipe Costing Card model (`fnb.recipe`) with real-time portion unit economics.
  - Raw material waste / shrinkage percentage adjustment factor on ingredient lines.
  - Dedicated packaging & disposables costing layer (cups, lids, straws, boxes).
  - Visual margin health status badges (Optimal $\ge 65\%$, Moderate $50\%-64\%$, Low $< 50\%$).
  - Interactive forward and reverse price simulation modal wizard (`fnb.recipe.simulate.wizard`).
  - 1-Click catalog product synchronization (`product.product`).
  - Root App Launcher icon and menu hierarchy.
  - Realistic café and kitchen demo recipes seeded.
- **Multi-Version Coverage:**
  - Added official support and created branch `19.0` alongside `18.0` and `20.0`.
  - Updated repository banners and badges to reflect `Odoo 18.0 | 19.0 | 20.0`.

---

## [1.2.0] - 2026-11-16

### Added
- **Official Brand Identity Kit (`BRANDKIT.md`):**
  - Standardized geometric vector iconography system matching Odoo's native design tokens.
  - Complete color palette tables (Aubergine `#985184`, Mint `#1AD3BB`, Tangerine `#F86126`, Gold `#FBB945`, Azure `#088BF5`, Petrol `#005E7A`).
  - Symmetrical interlocking geometric prism master logo.
  - High-resolution GitHub repository hero banner (1280x640).
  - Ready-to-use shields.io badges and anti-slop rules.

---

## [1.1.0] - 2026-11-16

### Added
- **`l10n_id_coretax_taxation` (Phase 1 Completed):**
  - 16-digit NIK/NPWP16 and 22-digit NITKU validation on partner contacts (PMK 112/PMK.03/2022).
  - Statutory withholding tax system (PPN 12%, PPh 21, 22, 23, 4(2), and PPh Final UMKM 0.5% PP 20/2026).
  - Automated sequential NSFP (Nomor Seri Faktur Pajak) quota range pool allocator.
  - Statutory e-Faktur 4.0 (`FK`/`OF`) and e-Bupot Coretax CSV batch exporters.
- **`marketplace_settlement_sync` (Phase 2 Completed):**
  - Omnichannel settlement statement importer for Shopee, Tokopedia, and TikTok Shop.
  - Split-accounting engine separating Gross Order Turnover, Platform Service Fees, and Net Escrow Deposits into General Ledger journals.

---

## [1.1.0] - 2026-11-16

### Added (Phase 6: QBiz Dynamic QRIS Integration)
- **Core Module `account_qris_qbiz`:** Integrated dynamic QRIS generator and automated bank mutation reconciler ported from [ardianryan/qbiz-qrisdinamis](https://github.com/ardianryan/qbiz-qrisdinamis).
- **EMVCo Engine (`models/qris_emvco.py`):** Standalone pure Python TLV parser, dynamic Tag 54 injection, and Bank Indonesia/ASPI compliant CCITT-16 CRC recalculation (polynomial `0x1021`, initial `0xFFFF`).
- **Unique Code Engine:** Automatic 3-digit anti-collision nominal suffix ensuring collision-free matching across concurrent customer payments.
- **Inbound Webhook Controller (`controllers/qris_webhook.py`):** Public JSON endpoint at `/api/v1/webhook/qris` for instant real-time settlement and automated journal entry reconciliation.
- **Invoice & Report Integration (`views/account_move_views.xml`, `views/report_invoice_qris.xml`):** Header actions, dynamic QR canvas preview, tree view status badges, and official PDF invoice QWeb overlay.
- **Master Banner & Assets:** Updated master branding banner (`assets/banner.svg` & `assets/banner.png`) to showcase all 6 active production modules.

---

## [1.0.0] - 2026-11-16

### Added
- Initial project architecture and repository structure under LGPL-3.0.
- Starter template module (`sample_app`).
- Architectural roadmap and technical specifications (`ROADMAP.md`).
- Community documentation suite: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CITATION.bib`.
