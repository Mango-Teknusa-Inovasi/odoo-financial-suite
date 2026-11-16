# Changelog

All notable changes to the **MangoTek Financial Suite** are documented in this file.

The format follows standard semantic versioning practices (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Planned
- Continuous integration testing and multi-company automated demo benchmarks.

---

## [1.5.0] - 2026-11-16

### Added
- **`financial_health_dashboard` (Phase 5 Completed):**
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

## [1.0.0] - 2026-11-16

### Added
- Initial project architecture and repository structure under LGPL-3.0.
- Starter template module (`sample_app`).
- Architectural roadmap and technical specifications (`ROADMAP.md`).
- Community documentation suite: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CITATION.bib`.
