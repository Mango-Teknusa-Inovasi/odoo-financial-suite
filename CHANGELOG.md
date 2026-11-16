# Changelog

All notable changes to the **MangoTek Financial Suite** are documented in this file.

The format follows standard semantic versioning practices (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Planned
- **`account_stamp_signature`** (Phase 4):
  - Dynamic company stamp and digital signature positioning on PDF customer invoices and purchase orders.
- **`financial_health_dashboard`** (Phase 4):
  - Executive financial ratio KPI widgets (Current, Quick, Debt-to-Equity, Net Margin).

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
