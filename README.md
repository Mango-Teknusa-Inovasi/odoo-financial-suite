# Odoo Financial Suite

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](LICENSE)
[![Odoo Version](https://img.shields.io/badge/Odoo-18.0%20%7C%2020.0-purple.svg)](https://www.odoo.com/)
[![Maintained by](https://img.shields.io/badge/Maintained%20by-Mango--Teknusa--Inovasi-orange.svg)](https://github.com/Mango-Teknusa-Inovasi)

An enterprise-ready financial and operational localization suite for Odoo, tailored to streamline Indonesian regulatory compliance, tax obligations, multi-channel commerce reconciliation, and light manufacturing costing.

---

## 🌟 Overview

Standard ERP systems often introduce significant administrative overhead when applied to Indonesian business landscapes. The **Odoo Financial Suite** bridges this gap by delivering modular extensions that integrate smoothly with Odoo's native ORM and accounting framework.

### Core Modules

* **`l10n_id_coretax_taxation`**: Comprehensive withholding tax compliance (PPh 21, 22, 23, 4(2), and MSME Final Tax PP 20/2026), 16-digit NPWP, NITKU management, and direct export routines compatible with the DJP Coretax portal.
* **`marketplace_settlement_sync`**: Automated settlement ingestion for Indonesian e-commerce platforms (Shopee, Tokopedia, TikTok Shop) with automated fee separation and daily journal aggregation.
* **`fnb_hpp_calculator`**: Simplified recipe costing and margin tracking designed for F&B and retail businesses without requiring heavyweight MRP modules.
* **`account_stamp_signature`**: Automated digital stamp and signature positioning for PDF invoices and purchase orders.
* **`financial_health_dashboard`**: Interactive financial ratios (Liquidity, Solvency, Profitability) featuring visual status indicators.

---

## 📂 Repository Layout

```text
odoo-financial-suite/
├── sample_app/                  # Starter development scaffold
├── l10n_id_coretax_taxation/    # Indonesian taxation & Coretax module
├── marketplace_settlement_sync/ # E-commerce settlement importer
├── fnb_hpp_calculator/          # Lightweight recipe costing
├── account_stamp_signature/     # PDF document seal overlay
├── financial_health_dashboard/  # Executive KPI and ratio widgets
├── CHANGELOG.md                 # Release notes and version history
├── CONTRIBUTING.md              # Development and contribution guide
├── CODE_OF_CONDUCT.md           # Community guidelines
├── SECURITY.md                  # Security policy and disclosure
├── CITATION.bib                 # Citation metadata
└── ROADMAP.md                   # Long-term architectural milestones
```

---

## 🚀 Getting Started

### Prerequisites

* Odoo 18.0 or 20.0 (Community or Enterprise)
* PostgreSQL 15+
* Python 3.10+

### Installation

1. Clone this repository into your Odoo custom addons directory:
   ```bash
   git clone https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite.git
   ```

2. Add the directory to your `odoo.conf`:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/odoo-financial-suite
   ```

3. Restart your Odoo server instance:
   ```bash
   python3 odoo-bin -c /etc/odoo/odoo.conf -u base
   ```

4. Navigate to **Apps** in your Odoo instance, activate **Developer Mode**, select **Update Apps List**, and install your desired modules.

---

## 👥 Authors & Maintainers

* **Mango Teknusa Inovasi** ([@Mango-Teknusa-Inovasi](https://github.com/Mango-Teknusa-Inovasi))

---

## 📄 License

This software suite is licensed under the GNU Lesser General Public License v3.0 (LGPL-3.0). Refer to the [LICENSE](LICENSE) file for complete details.
