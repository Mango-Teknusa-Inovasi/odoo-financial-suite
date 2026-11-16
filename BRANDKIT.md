# MangoTek Financial Suite — Brand Identity Kit (Brandkit)

> **Official Visual Identity, Design Tokens & Design System Guidelines for Odoo 18.0 & 20.0 Applications**  
> **Maintained by:** [Mango Teknusa Inovasi](https://github.com/Mango-Teknusa-Inovasi) · **Contact:** `billing@ppti.me`  
> **License:** 100% Free & Open Source under [LGPL-3.0](LICENSE)

---

## 1. Brand Mission & Positioning

**MangoTek Financial Suite** is the premier open-source localization, regulatory compliance, and multi-channel financial engine designed natively for the **Odoo** ERP ecosystem (compatible with Odoo 18.0 and 20.0, Community and Enterprise editions).

### Brand Essence
* **Native Harmony:** Feels like a first-party component built directly by Odoo SA.
* **Fiscal Precision:** Grounded in statutory Indonesian accounting and DJP Coretax compliance.
* **Democratic Open Source:** 100% free forever for the global Odoo community. Zero vendor lock-in.
* **Anti-Slop Craftsmanship:** Pure geometric vector geometry, purposeful facet shading, and intentional typography without generic AI hallucinations or skeuomorphic clutter.

---

## 2. Visual Architecture & Logo Anatomy

The master logo of **MangoTek Financial Suite** represents the seamless synthesis of **MangoTek's** dynamic commercial drive with **Odoo's** iconic geometric facet design language.

```
       [ Mango Tangerine ]       [ Odoo Aubergine ]
          Facet (#F86126)           Facet (#985184)
               \                         /
                \                       /
                 [ Central Fiscal Prism ]
                  Emerald Mint (#1AD3BB)
                  + Deep Petrol (#005E7A)
                /                       \
               /                         \
      [ Sunflower Gold ]         [ Enterprise Azure ]
       Facet (#FBB945)             Facet (#088BF5)
```

### Geometric Principles
1. **Base Canvas:** `50x50` standard Odoo grid (`viewBox="0 0 50 50"`).
2. **Corner Radii:** Outer boundary corners utilize `rx="4"` (or `r="4"`) for friendly curvature matching Odoo's backend UI.
3. **Facet Angles:** Precise diagonal cuts (angled at $45^\circ$ or $26.5^\circ$ / slope $1:2$) create dynamic depth without relying on blurry drop-shadows.
4. **Plane Hierarchy:** Flat solid fills placed on overlapping coordinate planes simulate three-dimensional refraction.

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

### 5. `financial_health_dashboard` (Executive Financial Health)
* **Concept:** Ascending multi-tier ratio bars (Solvency, Liquidity, Profitability) intersected by an upward growth vector diamond.
* **Palette:** Plum (`#985184`), Emerald Mint (`#1AD3BB`), Sunflower Gold (`#FBB945`), Coral (`#FC868B`), Tangerine (`#F86126`).
* **Source:** `assets/icons/financial_health_dashboard.svg`

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
  * **Category / Overline:** 11px–12px, Bold (700), letter-spacing `+1.5px` (All-caps)
  * **Body Copy:** 13px–15px, Regular (400), line-height `1.5`

---

## 6. Sizing & Export Specifications

All icons and brand assets are maintained in vector SVG and exported to raster PNG formats for diverse consumption channels:

| Asset | Resolution | Format | Purpose |
|:---|:---|:---|:---|
| **App Launcher Icon** | `50x50` (or `100x100` @2x) | PNG / SVG | Odoo 9-dots App Drawer & Kanban Views |
| **Odoo Apps Store Thumbnail** | `512x512` | PNG / SVG | Odoo Apps Store Listing & Vendor Portal |
| **GitHub Master Banner** | `1280x640` | PNG / SVG | GitHub Social Card & README Hero Header |
| **Favicon** | `32x32` / `16x16` | PNG / ICO | Web browser tab indicator |

---

## 7. Anti-Slop Brand Rules

* **DO:** Use solid geometric shapes with sharp crisp lines and mathematical corner radii.
* **DO:** Maintain high-contrast facet boundaries so icons remain legible down to 24px.
* **DO:** Always display the official `100% Free & Open Source · LGPL-3.0` badge on public listings.
* **DON'T:** Never apply generic AI gradient bubbles, glossy chrome reflections, or skeuomorphic glassmorphism.
* **DON'T:** Never distort the aspect ratio ($1:1$ for icons, $2:1$ for the repository banner).
* **DON'T:** Never introduce third-party proprietary vendor logos into open-source core assets.
