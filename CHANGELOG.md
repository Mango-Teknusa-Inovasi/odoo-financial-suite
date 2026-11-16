# Changelog

All notable changes to the **Odoo Financial Suite** project are documented in this file.

The format follows standard semantic versioning practices (`MAJOR.MINOR.PATCH`).

---

## [Unreleased]

### Planned
- **`l10n_id_coretax_taxation`**:
  - 16-digit NPWP and 22-digit NITKU validation on partner records.
  - Automatic withholding tax deduction workflows for PPh 21, PPh 22, PPh 23, and PPh 4(2).
  - PPh Final UMKM 0.5% computation under Government Regulation PP 20/2026.
  - CSV export wizard compatible with DJP Coretax schema.
- **`marketplace_settlement_sync`**:
  - Ingestion wizards for Shopee, Tokopedia, and TikTok Shop daily settlement statements.
  - Automated journal generation separating gross revenues from marketplace service deductions.
- **`fnb_hpp_calculator`**:
  - Direct recipe card calculation converting raw ingredient bulk purchases into portion costs.
- **`account_stamp_signature`**:
  - QWeb report overlay for semi-transparent company stamps over authorized digital signatures.
- **`financial_health_dashboard`**:
  - Executive financial health indicator widgets for balance sheet liquidity and operating margin ratios.

---

## [1.0.0] - 2026-11-16

### Added
- Initial project architecture and repository structure.
- Starter template module (`sample_app`) demonstrating standard Odoo 18.0/20.0 MVC conventions.
- Architectural roadmap and technical specifications (`ROADMAP.md`).
- Community documentation suite: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CITATION.bib`.
