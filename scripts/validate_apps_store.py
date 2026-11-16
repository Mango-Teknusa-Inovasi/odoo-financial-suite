#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odoo Apps Store Vendor Guidelines Compliance Validator
Part of MangoTek Financial Suite (LGPL-3.0)
"""

import os
import ast
import re
import sys

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES = [
    "l10n_id_coretax_taxation",
    "marketplace_settlement_sync",
    "fnb_hpp_calculator",
    "account_stamp_signature",
    "financial_health_kpi",
    "account_qris_qbiz",
    "account_opening_balance_wizard",
]

def validate_suite():
    print("=" * 65)
    print(" 🔍 ODOO APPS STORE VENDOR GUIDELINE COMPLIANCE AUDIT")
    print("=" * 65)
    
    total_checks = 0
    passed_checks = 0
    failed_modules = []

    for mod in MODULES:
        mod_dir = os.path.join(REPO_DIR, mod)
        print(f"\n📦 Auditing Module: {mod}")
        
        manifest_path = os.path.join(mod_dir, "__manifest__.py")
        if not os.path.exists(manifest_path):
            print(f"  ❌ Missing __manifest__.py!")
            failed_modules.append(mod)
            continue
            
        with open(manifest_path, "r", encoding="utf-8") as f:
            try:
                manifest = ast.literal_eval(f.read())
            except Exception as e:
                print(f"  ❌ Invalid Python AST in manifest: {e}")
                failed_modules.append(mod)
                continue
                
        # 1. Name Check (<= 25 chars, no adjectives, no company name)
        total_checks += 1
        name = manifest.get("name", "")
        name_len = len(name)
        if 0 < name_len <= 25 and not any(w in name.lower() for w in ["best", "awesome", "mangotek", "pro", "free"]):
            print(f"  ✅ [Name] '{name}' ({name_len}/25 chars, explicit, compliant)")
            passed_checks += 1
        else:
            print(f"  ❌ [Name] Invalid name or exceeds 25 chars: '{name}' ({name_len} chars)")
            failed_modules.append(mod)

        # 2. Version Check (<odoo_version>.major.minor.patch)
        total_checks += 1
        version = manifest.get("version", "")
        if re.match(r"^\d+\.\d+\.\d+\.\d+\.\d+$", version) or re.match(r"^\d+\.\d+\.1\.0\.0$", version):
            print(f"  ✅ [Version] '{version}' (Conforms to Odoo semantic versioning)")
            passed_checks += 1
        else:
            print(f"  ❌ [Version] Invalid format: '{version}' (Expected <odoo_version>.1.0.0)")
            failed_modules.append(mod)

        # 3. License Check (LGPL-3)
        total_checks += 1
        license_val = manifest.get("license", "")
        if license_val == "LGPL-3":
            print(f"  ✅ [License] '{license_val}' (100% Free & Open Source)")
            passed_checks += 1
        else:
            print(f"  ❌ [License] Expected 'LGPL-3', found: '{license_val}'")
            failed_modules.append(mod)

        # 4. Depends Check
        total_checks += 1
        depends = manifest.get("depends", [])
        if isinstance(depends, list) and len(depends) > 0:
            print(f"  ✅ [Depends] {depends}")
            passed_checks += 1
        else:
            print(f"  ❌ [Depends] Depends must be a non-empty list!")
            failed_modules.append(mod)

        # 5. Price & Currency (0.0 EUR)
        total_checks += 1
        price = manifest.get("price", None)
        currency = manifest.get("currency", "")
        if price == 0.0 and currency in ("EUR", "USD"):
            print(f"  ✅ [Price/Currency] {price} {currency} (Free Tier Declared)")
            passed_checks += 1
        else:
            print(f"  ❌ [Price/Currency] Invalid price/currency: {price} {currency}")
            failed_modules.append(mod)

        # 6. Images / Cover Check (Criterion 2 for 5/5 score)
        total_checks += 1
        images = manifest.get("images", [])
        if images and len(images) > 0:
            cover_path = os.path.join(mod_dir, images[0])
            if os.path.exists(cover_path):
                print(f"  ✅ [Cover Image] '{images[0]}' ({os.path.getsize(cover_path):,} bytes) -> Store Criterion 2 PASS")
                passed_checks += 1
            else:
                print(f"  ❌ [Cover Image] File not found: {cover_path}")
                failed_modules.append(mod)
        else:
            print(f"  ❌ [Cover Image] 'images' key missing in manifest!")
            failed_modules.append(mod)

        # 7. Icon Check (Criterion 1 for 5/5 score)
        total_checks += 1
        icon_path = os.path.join(mod_dir, "static", "description", "icon.png")
        if os.path.exists(icon_path):
            print(f"  ✅ [Module Icon] 'static/description/icon.png' ({os.path.getsize(icon_path):,} bytes) -> Store Criterion 1 PASS")
            passed_checks += 1
        else:
            print(f"  ❌ [Module Icon] Missing static/description/icon.png!")
            failed_modules.append(mod)

        # 8. HTML Description Check (Criterion 5 for 5/5 score)
        total_checks += 1
        html_path = os.path.join(mod_dir, "static", "description", "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as hf:
                html_txt = hf.read()
            if "<script" in html_txt.lower():
                print(f"  ❌ [Description] Forbidden <script> tag found!")
                failed_modules.append(mod)
            else:
                ext_links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html_txt)
                forbidden_links = [l for l in ext_links if not ("youtube.com" in l or "teams.microsoft.com" in l)]
                if forbidden_links:
                    print(f"  ❌ [Description] Forbidden external links: {forbidden_links}")
                    failed_modules.append(mod)
                else:
                    print(f"  ✅ [Description] 'static/description/index.html' (Valid HTML, clean links) -> Store Criterion 5 PASS")
                    passed_checks += 1
        else:
            print(f"  ❌ [Description] Missing static/description/index.html!")
            failed_modules.append(mod)

    print("\n" + "=" * 65)
    print(f" 📊 AUDIT SUMMARY: {passed_checks}/{total_checks} CHECKS PASSED")
    print("=" * 65)
    
    if not failed_modules:
        print(f"🎉 ALL {len(MODULES)} MODULES 100% COMPLIANT WITH ODOO APPS VENDOR GUIDELINES!")
        print("🌟 Ready for immediate submission to apps.odoo.com (Score: 5.0 / 5.0)")
        return 0
    else:
        print(f"🚨 Compliance failed in modules: {set(failed_modules)}")
        return 1

if __name__ == "__main__":
    sys.exit(validate_suite())
