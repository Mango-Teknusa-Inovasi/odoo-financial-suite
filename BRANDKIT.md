# MangoTek Financial Suite — Brand Identity Kit (Brandkit)

> **Official Visual Identity, Design Tokens & Design System Guidelines for Odoo 18.0, 19.0 & 20.0 Applications**  
> **Maintained by:** [Mango Teknusa Inovasi](https://github.com/Mango-Teknusa-Inovasi) · **Contact:** `billing@ppti.me`  
> **License:** 100% Free & Open Source under [LGPL-3.0](LICENSE)

---

## 1. Brand Mission & Positioning

**MangoTek Financial Suite** is the premier open-source localization, regulatory compliance, and multi-channel financial engine designed natively for the **Odoo** ERP ecosystem (compatible with Odoo 18.0, 19.0 and 20.0, Community and Enterprise editions).

### Brand Essence
* **Native Harmony:** Feels like a first-party component built directly by Odoo SA.
* **Fiscal Precision:** Grounded in statutory Indonesian accounting and DJP Coretax compliance.
* **Democratic Open Source:** 100% free forever for the global Odoo community. Zero vendor lock-in.
* **Anti-Slop Craftsmanship:** Pure geometric vector geometry, purposeful facet shading, and intentional typography without generic AI hallucinations or skeuomorphic clutter.

---

## 2. Master Logo Anatomy: The MangoTek Geometric Prism

The master logo of **MangoTek Financial Suite** embodies the crisp, multi-faceted geometric design language of native Odoo applications: a precision interlocking squircle prism composed of six harmonic facet polygons.

```
          [ Odoo Plum #985184 ] --- [ Sunflower Gold #FBB945 ]
                    \                      /
                     \                    /
                      [ Mint Gem #1AD3BB ]
                      [ Shadow #005E7A  ]
                     /                    \
                    /                      \
        [ Tangerine #F86126 ] --- [ Royal Azure #088BF5 ]
```

### Geometric Principles
1. **Silhouette Test:** Instantly recognizable as a stylized, premium Mango fruit silhouette with a top emerald leaf.
2. **Base Canvas:** `50x50` standard Odoo grid (`viewBox="0 0 50 50"`).
3. **Core Monogram:** Symmetrical capital letter "M" anchored in the center, ensuring strong identity even at 16px favicon scale.
4. **Facet Angles:** Clean diagonal cuts ($45^\circ$ and $60^\circ$) create dynamic depth without using skeuomorphic gradients or drop-shadows.

---

## 3. Official Color Palette & Design Tokens

The color system directly incorporates and complements Odoo's official branding palette, enriched with Indonesian fiscal emerald and warm commercial citrus tones.

| Role | Color Name | Hex Code | RGB | Semantic Function |
|:---|:---|:---|:---|:---|
| **Primary Odoo** | Amethyst Aubergine | `#985184` | `rgb(152, 81, 132)` | Odoo heritage, accounting ledger facets, core stability |
| **Fiscal Accent** | Emerald Mint | `#1AD3BB` | `rgb(26, 211, 187)` | DJP Coretax certification, positive cashflow, reconciliation |
| **Commerce Warm** | Mango Tangerine | `#F86126` | `rgb(248, 97, 38)` | Indonesian marketplace energy, Shopee settlement, retail |
| **Gold Standard** | Sunflower Amber | `#FBB945` | `rgb(251, 185, 69)` | Official seals, Tokopedia gold, recipe costing valuation |
| **Corporate Tech** | Royal Azure | `#088BF5` | `rgb(8, 139, 245)` | Document stamping, official e-Meterai, cloud automation |
| **Light Accent** | Sky Cyan | `#2EBCFA` | `rgb(46, 188, 250)` | Secondary highlights, digital flow arrows, trendlines |
| **Depth Shading** | Deep Petrol Slate | `#005E7A` | `rgb(0, 94, 122)` | Facet shading, high-contrast borders, technical elements |
| **Canvas Dark** | Midnight Navy | `#0B0F19` | `rgb(11, 15, 25)` | GitHub banners, hero cards, dark-mode backgrounds |

---

## 4. Module Iconography System

Each module in the MangoTek Financial Suite possesses a distinct, cohesive 50x50 vector icon adhering to the master design rules:

### 1. `l10n_id_coretax_taxation` (Indonesian Tax Coretax)
* **Concept:** Official fiscal folio with folded dog-ear corner, statutory ribbon, and golden DJP tax seal with geometric `%` symbol.
* **Palette:** Emerald Mint (`#1AD3BB`), Sunflower Gold (`#FBB945`), Tangerine (`#F86126`), Deep Petrol (`#005E7A`), Aubergine (`#985184`).
* **Source:** `assets/icons/l10n_id_coretax_taxation.svg`

### 2. `marketplace_settlement_sync` (Marketplace Settlement)
* **Concept:** Multi-channel storefront tote fused with an accounting ledger card and interlocking dual sync flow arrows.
* **Palette:** Tangerine (`#F86126`), Sunflower Gold (`#FBB945`), Plum (`#985184`), Emerald Mint (`#1AD3BB`), Sky Cyan (`#2EBCFA`).
* **Source:** `assets/icons/marketplace_settlement_sync.svg`

### 3. `fnb_hpp_calculator` (F&B Recipe HPP Costing)
* **Concept:** Professional culinary cloche base overlapping an interactive math calculator badge with percentage and plus operators.
* **Palette:** Plum (`#985184`), Sunflower Gold (`#FBB945`), Tangerine (`#F78613`), Emerald Mint (`#1AD3BB`), Deep Petrol (`#005E7A`).
* **Source:** `assets/icons/fnb_hpp_calculator.svg`

### 4. `account_stamp_signature` (Digital Stamp & e-Meterai)
* **Concept:** Commercial invoice document fold stamped with an official notched e-Meterai seal and rosette emblem.
* **Palette:** Royal Azure (`#088BF5`), Sky Cyan (`#2EBCFA`), Midnight Navy (`#144496`), Coral Red (`#F06050`), Sunflower Gold (`#FBB945`).
* **Source:** `assets/icons/account_stamp_signature.svg`

### 5. `financial_health_kpi` (Executive Financial Health)
* **Concept:** Ascending multi-tier ratio bars (Solvency, Liquidity, Profitability) intersected by an upward growth vector diamond.
* **Palette:** Plum (`#985184`), Emerald Mint (`#1AD3BB`), Sunflower Gold (`#FBB945`), Coral (`#FC868B`), Tangerine (`#F86126`).
* **Source:** `assets/icons/financial_health_kpi.svg`

### 6. `account_qris_qbiz` (QBiz Dynamic QRIS)
* **Concept:** Interlocking four-corner QR positioning targets framing dynamic lightning bolt payment mutation vectors.
* **Palette:** Royal Azure (`#088BF5`), Sky Cyan (`#2EBCFA`), Deep Petrol (`#005E7A`), Emerald Mint (`#1AD3BB`).
* **Source:** `account_qris_qbiz/static/description/icon.png`

### 7. `account_opening_balance_wizard` (Opening Balance Setup Wizard)
* **Concept:** Symmetrical double-entry balance scale with ascending foundation blocks and ledger migration arrows.
* **Palette:** Sunflower Amber (`#D97706`), Warm Tangerine (`#F86126`), Deep Petrol (`#005E7A`), Emerald Mint (`#1AD3BB`).
* **Source:** `account_opening_balance_wizard/static/description/icon.png`

### 8. `account_whatsapp_notifier` (WhatsApp Finance Notifier)
* **Concept:** Multi-device chat bubble containing verified invoice document fold, dispatch arrow, and payment settlement checks.
* **Palette:** WhatsApp Green (`#25D366`), Emerald Mint (`#1AD3BB`), Royal Azure (`#088BF5`), Deep Petrol (`#005E7A`).
* **Source:** `account_whatsapp_notifier/static/description/icon.png`

### 9. `account_project_job_costing` (Project Job Costing)
* **Concept:** Dual-metric project cost sheet with geometric budget progress bars, cashflow liquidity indicators, and contractor cost categories.
* **Palette:** Royal Sky Azure (`#0284C7`), Midnight Slate (`#0F172A`), Emerald Mint (`#1AD3BB`), Tangerine (`#F86126`).
* **Source:** `account_project_job_costing/static/description/icon.png`

### 10. `pos_thermal_receipt_designer` (POS Thermal Receipt)
* **Concept:** Continuous thermal receipt paper roll featuring zigzag tear edges, monospace line grid, monochrome barcode/QRIS, and printer feed roll.
* **Palette:** Sunflower Amber (`#F59E0B`), Midnight Slate (`#0F172A`), Pure Paper White (`#FFFFF8`), Emerald Mint (`#1AD3BB`).
* **Source:** `pos_thermal_receipt_designer/static/description/icon.png`

---

## 5. Typography Standards

* **Primary Font Family:** System font stack mimicking Odoo's backend UI:
  ```css
  font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  ```
* **Type Hierarchy:**
  * **Hero Title:** 40px–44px, ExtraBold (800), letter-spacing `-0.5px`
  * **Section Heading:** 24px–28px, Bold (700)
  * **Subheading / Card Title:** 14px–16px, SemiBold (600)
  * **Category / Overline:** 11px–12px, Bold (700), letter-spacing `+2.0px` (All-caps)
  * **Body Copy:** 13px–15px, Regular (400), line-height `1.5`

---

## 6. Sizing & Export Specifications

All icons and brand assets are maintained in vector SVG and exported to raster PNG formats for diverse consumption channels:

| Asset | Resolution | Format | Purpose |
|:---|:---|:---|:---|
| **App Launcher Icon** | `100x100` (or `50x50`) | PNG / SVG | Odoo 9-dots App Drawer & Kanban Views |
| **Module Cover Banner** | `1200x630` (1.905:1) | PNG | Odoo Apps Store Index & Module Header |
| **Odoo Apps Store Thumbnail** | `512x512` | PNG / SVG | Odoo Apps Store Listing & Vendor Portal |
| **GitHub Master Banner** | `1280x640` (2:1) | PNG / SVG | GitHub Social Card & README Hero Header |
| **Favicon** | `32x32` / `16x16` | PNG / ICO | Web browser tab indicator |

---

## 7. Anti-Slop Brand Rules

* **DO:** Use solid geometric shapes with sharp crisp lines and mathematical corner radii.
* **DO:** Maintain high-contrast facet boundaries so icons remain legible down to 24px.
* **DO:** Always display the official `100% Free & Open Source · LGPL-3.0` badge on public listings.
* **DON'T:** Never apply generic AI gradient bubbles, glossy chrome reflections, or skeuomorphic glassmorphism.
* **DON'T:** Never distort the aspect ratio ($1:1$ for icons, $1200\times630$ for module banners).
* **DON'T:** Never introduce third-party proprietary vendor logos into open-source core assets.

---

## 8. Standardized Module Banner Architecture & Governance

To eliminate visual inconsistency across the MangoTek Financial Suite (such as differing layouts, fonts, badge counts, or background styles), all module banners (`static/description/banner.png`) MUST strictly adhere to the unified architecture defined below and MUST be generated using `scripts/generate_module_banners.py`.

### Unified Banner Specification (1200 x 630 px)

```
+-------------------------------------------------------------------------------+
|  [● 100% FREE & OPEN SOURCE · LGPL-3]                                         |  py = 42
|                                                                               |
|                            [ 140x140 Icon Container ]                         |  y = 100..240
|                                                                               |
|                             MODULE TITLE (46px Bold)                          |  y = 280
|                                                                               |
|                       Feature Subtitle Description (21px)                     |  y = 350
|                                                                               |
|                      SUITE IDENTIFIER OVERLINE (13px Bold)                    |  y = 400
|                                                                               |
|   [🟣 Odoo 18.0, 19.0 & 20.0]  [✨ Module Specific Highlight]  [⚖️ Community]   |  y = 515
+-------------------------------------------------------------------------------+
```

### Visual Anatomy Rules
1. **Canvas & Background:**
   - Dimensions: `1200 x 630` pixels exactly.
   - Background: Dark gradient from `#0F172A` (top) to `#182036` (bottom).
   - Radial Ambient Glow: Centered at `cx=600, cy=230` with `radius=320`, tinted with the module's primary `accent_rgb` at 15% opacity.
2. **Top Open Source Badge:**
   - Position: Centered horizontally at `py = 42`.
   - Text: `100% FREE & OPEN SOURCE · LGPL-3` in Segoe UI Bold 14px, letter-spaced `+1.5px`.
   - Indicator: Emerald green circle dot (`#10B981`, radius 4px) preceding the text.
   - Container: Rounded rectangle (`fill=#1E293B, outline=#334155, radius=18`).
3. **Module Icon Plate:**
   - Position: Centered at `x = 530..670, y = 100..240` (140x140 px).
   - Container: Rounded squircle (`fill=#1E293B, outline=#334155, radius=24`).
   - Icon Graphic: 100x100 px centered inside the plate.
4. **Typography & Hierarchical Positioning:**
   - **Title:** `y = 280`, Segoe UI Bold 46px, `#FFFFFF`.
   - **Subtitle:** `y = 350`, Segoe UI Regular 21px, `#94A3B8`.
   - **Suite Identifier:** `y = 400`, Segoe UI Bold 13px, tracking `+3.0px`, uppercase `#38BDF8`.
5. **Bottom Standard Pills (Strictly 3 Pills):**
   - Pill 1 (Framework): `🟣 Odoo 18.0, 19.0 & 20.0`
   - Pill 2 (Highlight): Specific core capability (e.g. `⚡ ASPI QRIS & Webhook`, `⚖️ Dynamic Net Equity Balancing`)
   - Pill 3 (Tier): `⚖️ Community & Enterprise`
   - Styling: Rounded capsules (`radius=16, fill=#1E293B, outline=#334155`), text 14px SemiBold `#E2E8F0`.

### Master Generator Script
Any addition of new modules or updates to banners must be executed via:
```bash
python scripts/generate_module_banners.py
```
This guarantees 100% visual parity across all modules in the repository without manual graphical discrepancies.
