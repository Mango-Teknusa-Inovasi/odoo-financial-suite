# -*- coding: utf-8 -*-
"""
MangoTek Financial Suite — Standardized Module Banner Generator
Generates pixel-perfect, 1200x630 cover banners for all Odoo modules
in strict accordance with BRANDKIT.md and the Anti-Slop Design System.
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(REPO_ROOT, 'assets', 'icons')

# Design System Palette Tokens (from BRANDKIT.md)
PALETTE = {
    'midnight_navy': (15, 23, 42),       # #0F172A Base Canvas
    'gradient_bottom': (24, 32, 54),     # Bottom Canvas Shading
    'slate_card': (30, 41, 59),          # #1E293B Container Fill
    'slate_border': (51, 65, 85),        # #334155 Border Stroke
    'text_primary': (255, 255, 255),     # Pure White Titles
    'text_muted': (148, 163, 184),       # #94A3B8 Subtitles
    'emerald_mint': (26, 211, 187),      # #1AD3BB Fiscal Accent
    'emerald_bg': (16, 45, 45),          # Top Badge Background
    'odoo_plum': (113, 75, 103),         # Odoo Version Badge Fill
    'odoo_plum_border': (160, 110, 145), # Odoo Version Badge Border
    'pill_neutral_border': (71, 85, 105),# Neutral Badge Border
}

MODULE_SPECIFICATIONS = [
    {
        "dir": "l10n_id_coretax_taxation",
        "icon": "l10n_id_coretax_taxation_512.png",
        "title": "Indonesian Tax Coretax",
        "subtitle": "DJP Coretax 2026 · e-Faktur 4.0 · PPN 12% · Withholding Tax (PPh)",
        "accent": (26, 211, 187), # Emerald Mint
        "highlight": "⚡ DJP e-Faktur 4.0 & Coretax CSV",
    },
    {
        "dir": "marketplace_settlement_sync",
        "icon": "marketplace_settlement_sync_512.png",
        "title": "Marketplace Settlement",
        "subtitle": "Shopee · Tokopedia · TikTok Shop Statement Ingestion & Split-Accounting",
        "accent": (248, 97, 38), # Tangerine
        "highlight": "🛒 Shopee · Tokopedia · TikTok",
    },
    {
        "dir": "fnb_hpp_calculator",
        "icon": "fnb_hpp_calculator_512.png",
        "title": "F&B Recipe HPP",
        "subtitle": "Culinary Recipe Costing · Portion Margin · Wastage Factor · POS Sync",
        "accent": (245, 158, 11), # Sunflower Amber
        "highlight": "🍽️ Recipe Costing & POS Sync",
    },
    {
        "dir": "account_stamp_signature",
        "icon": "account_stamp_signature_512.png",
        "title": "Stamp & e-Meterai",
        "subtitle": "Transparent Wet Seal Overlay (-6°) · Peruri e-Meterai Gateway (UU 10/2020)",
        "accent": (8, 139, 245), # Royal Azure
        "highlight": "⚖️ Peruri e-Meterai & Wet Seal",
    },
    {
        "dir": "financial_health_kpi",
        "icon": "financial_health_kpi_512.png",
        "title": "Financial Health KPI",
        "subtitle": "Executive Financial Ratios · Liquidity & Solvency · Traffic-Light Scorecard",
        "accent": (152, 81, 132), # Odoo Plum
        "highlight": "📊 Real-Time Ratio KPI Scorecard",
    },
    {
        "dir": "account_qris_qbiz",
        "icon": "account_qris_qbiz_512.png",
        "title": "QBiz Dynamic QRIS",
        "subtitle": "Dynamic QRIS Invoicing · Tag 54 Injection · CRC16 · Webhook Auto-Reconciliation",
        "accent": (8, 139, 245), # Royal Azure
        "highlight": "💳 QBiz Dynamic QRIS & POS",
    },
    {
        "dir": "account_opening_balance_wizard",
        "icon": "account_opening_balance_wizard_512.png",
        "title": "Opening Balance Wizard",
        "subtitle": "1-Page Indonesian Opening Balance Setup · Auto-Equity Balancing · Asset & Stock Init",
        "accent": (26, 211, 187), # Emerald Mint
        "highlight": "⚖️ 1-Page Setup & Auto-Equity",
    },
    {
        "dir": "account_whatsapp_notifier",
        "icon": "account_whatsapp_notifier_512.png",
        "title": "WhatsApp Finance Notifier",
        "subtitle": "1-Click WhatsApp Invoicing · GOWA Multi-Device Bridge · PDF Dispatch",
        "accent": (37, 211, 102), # WhatsApp Green
        "highlight": "💬 GOWA & WhatsApp Dispatch",
    },
    {
        "dir": "account_project_job_costing",
        "icon": "account_project_job_costing_512.png",
        "title": "Project Job Costing",
        "subtitle": "Agile Project Cost Sheet · Dual-Metric Accrual & Cashflow · Budget Burn Rate",
        "accent": (2, 132, 199), # Royal Sky Azure (#0284C7)
        "highlight": "📈 Dual-Metric Accrual & Cashflow",
    },
    {
        "dir": "pos_thermal_receipt_designer",
        "icon": "pos_thermal_receipt_designer_512.png",
        "title": "POS Thermal Receipt",
        "subtitle": "Dual-Engine ESC/POS & QWeb · 58/80mm Adaptive Layout · Dynamic QRIS",
        "accent": (245, 158, 11), # Sunflower Amber
        "highlight": "🖨️ ESC/POS & 58/80mm Thermal",
    },
    {
        "dir": "l10n_id_bi_currency_rate",
        "icon": "l10n_id_bi_currency_rate_512.png",
        "title": "BI Currency Rate Sync",
        "subtitle": "Official Bank Indonesia JISDOR · Kurs Transaksi BI · KMK Tax Rates",
        "accent": (16, 185, 129), # Emerald Green (#10B981)
        "highlight": "🏛️ BI JISDOR & KMK Tax Rates",
    },
]

def get_font(font_name, size):
    """Attempt to load Windows standard font with graceful fallback."""
    candidate_paths = [
        f"C:/Windows/Fonts/{font_name}",
        f"/usr/share/fonts/truetype/dejavu/{font_name}",
        font_name
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("arialbd.ttf" if "b" in font_name else "arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def render_module_banner(mod):
    """Render a standardized 1200x630 Odoo Apps Store cover banner."""
    W, H = 1200, 630
    img = Image.new('RGB', (W, H), PALETTE['midnight_navy'])
    draw = ImageDraw.Draw(img)

    # 1. Subtle Linear Background Gradient
    top_r, top_g, top_b = PALETTE['midnight_navy']
    bot_r, bot_g, bot_b = PALETTE['gradient_bottom']
    for y in range(H):
        ratio = y / H
        r = int(top_r * (1 - ratio) + bot_r * ratio)
        g = int(top_g * (1 - ratio) + bot_g * ratio)
        b = int(top_b * (1 - ratio) + bot_b * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Ambient Lighting Glow behind Icon and Title
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    cx, cy = 600, 230
    accent = mod["accent"]
    for radius in range(320, 0, -10):
        alpha = int(28 * (1 - radius / 320))
        ov_draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                        fill=(accent[0], accent[1], accent[2], alpha))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

    # 3. Fonts Setup
    font_top = get_font('segoeuib.ttf', 15)
    font_title = get_font('segoeuib.ttf', 46)
    font_sub = get_font('segoeui.ttf', 21)
    font_cat = get_font('segoeuib.ttf', 13)
    font_pill = get_font('segoeuib.ttf', 15)

    # 4. Top Tag: 100% Free & Open Source Badge
    tag_text = '100% FREE & OPEN SOURCE · LGPL-3'
    tb = draw.textbbox((0, 0), tag_text, font=font_top)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    px, py = (W - tw) // 2, 42
    pad_x, pad_y = 18, 7
    draw.rounded_rectangle(
        [px - pad_x, py - pad_y, px + tw + pad_x, py + th + pad_y],
        radius=16,
        fill=PALETTE['emerald_bg'],
        outline=PALETTE['emerald_mint'],
        width=1
    )
    draw.ellipse([px - 8, py + 5, px - 2, py + 11], fill=PALETTE['emerald_mint'])
    draw.text((px + 5, py), tag_text, fill=PALETTE['emerald_mint'], font=font_top)

    # 5. Module Icon in Rounded Container
    icon_path = os.path.join(ASSETS_DIR, mod["icon"])
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert('RGBA')
        icon = icon.resize((140, 140), Image.Resampling.LANCZOS)
        icon_x = (W - 140) // 2
        icon_y = 100
        draw.rounded_rectangle(
            [icon_x - 12, icon_y - 12, icon_x + 140 + 12, icon_y + 140 + 12],
            radius=24,
            fill=PALETTE['slate_card'],
            outline=PALETTE['slate_border'],
            width=1
        )
        img.paste(icon, (icon_x, icon_y), icon)

    # 6. Module Title
    tb = draw.textbbox((0, 0), mod["title"], font=font_title)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 280), mod["title"], fill=PALETTE['text_primary'], font=font_title)

    # 7. Subtitle
    tb = draw.textbbox((0, 0), mod["subtitle"], font=font_sub)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 350), mod["subtitle"], fill=PALETTE['text_muted'], font=font_sub)

    # 8. Suite Category Overline
    cat_text = 'OFFICIAL MANGO-TEK FINANCIAL SUITE ADDON'
    tb = draw.textbbox((0, 0), cat_text, font=font_cat)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 400), cat_text, fill=accent, font=font_cat)

    # 9. Standardized 3-Pill Bottom Row
    pills = [
        ('🟣 Odoo 18.0, 19.0 & 20.0', PALETTE['odoo_plum'], PALETTE['odoo_plum_border']),
        (mod["highlight"], PALETTE['slate_card'], accent),
        ('⚖️ Community & Enterprise', PALETTE['slate_card'], PALETTE['pill_neutral_border']),
    ]

    total_pill_w = 0
    pill_widths = []
    for ptext, _, _ in pills:
        tb = draw.textbbox((0, 0), ptext, font=font_pill)
        w = (tb[2] - tb[0]) + 32
        pill_widths.append(w)
        total_pill_w += w
    total_pill_w += (len(pills) - 1) * 16  # 16px horizontal gap

    start_x = (W - total_pill_w) // 2
    cur_x = start_x
    pill_y = 515
    for i, (ptext, bg_col, border_col) in enumerate(pills):
        pw = pill_widths[i]
        draw.rounded_rectangle(
            [cur_x, pill_y, cur_x + pw, pill_y + 36],
            radius=18,
            fill=bg_col,
            outline=border_col,
            width=1
        )
        tb = draw.textbbox((0, 0), ptext, font=font_pill)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        draw.text((cur_x + (pw - tw) // 2, pill_y + (36 - th) // 2 - 2), ptext, fill=(241, 245, 249), font=font_pill)
        cur_x += pw + 16

    # 10. Save Banner
    out_dir = os.path.join(REPO_ROOT, mod["dir"], 'static', 'description')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'banner.png')
    img.save(out_path, 'PNG', optimize=True)
    print(f"✅ Generated {out_path} ({os.path.getsize(out_path)} bytes)")

def generate_all():
    print("=" * 65)
    print(" 🎨 STANDARDIZING MANGO-TEK MODULE BANNERS (BRANDKIT COMPLIANT)")
    print("=" * 65)
    for mod in MODULE_SPECIFICATIONS:
        render_module_banner(mod)
    print("=" * 65)
    print(" 🎉 ALL MODULE BANNERS UNIFIED WITH ZERO VARIATION!")

if __name__ == '__main__':
    generate_all()
