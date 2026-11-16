# Security Policy & OWASP Compliance Standard

**MangoTek Financial Suite (`odoo-financial-suite`)** is engineered for enterprise financial compliance, Indonesian statutory tax reporting (DJP Coretax 2026), dynamic electronic payment gateways, and accounting reconciliation. 

Security, data privacy, and isolation are paramount. This document outlines our security governance, architectural alignment with the **OWASP Top 10**, vulnerability disclosure guidelines, and supported release channels.

---

## 🛡️ Supported Versions & Security Maintenance

Security patches, CVE mitigations, and compliance hotfixes are actively maintained across the following Odoo series:

| Series | Supported | Release Channel | Security Maintenance Tier |
| :--- | :---: | :--- | :--- |
| **Odoo 20.0** | :white_check_mark: | `20.0` branch | **Active Support** (Primary development & cutting-edge features) |
| **Odoo 19.0** | :white_check_mark: | `19.0` branch | **Active Support** (Enterprise stable) |
| **Odoo 18.0** | :white_check_mark: | `18.0` branch | **Active Support** (LTS stable production baseline) |
| **< 18.0** | :x: | - | *End of Life (EOL)* — Community backports only |

---

## 🔒 OWASP Top 10 Security Alignment Matrix

The entire suite adheres to the **OWASP Top 10 Application Security Risks** through defensive coding, Odoo ORM invariants, and automated static security analysis:

| OWASP Risk | Technical Mitigation in MangoTek Financial Suite |
| :--- | :--- |
| **A01: Broken Access Control** | • **Model ACL:** Explicit permission matrix defined in `ir.model.access.csv` separating regular users (`read-only`) from financial managers (`full CRUD`).<br>• **Multi-Company Record Rules (`ir.rule`):** Strict tenant isolation enforcing `['\|', ('company_id', '=', False), ('company_id', 'in', company_ids)]` across all custom models (`fnb.recipe`, `marketplace.channel`, `l10n_id.nsfp.range`, `financial.health.kpi`, `emeterai.provider`).<br>• **Webhook Authorization:** Machine-to-machine endpoints require `X-QBiz-Api-Key` or Bearer token matching the company secret. |
| **A02: Cryptographic Failures** | • **Zero Plaintext Secrets:** Sensitive API keys (QBiz, e-Meterai providers) are masked in UI fields.<br>• **Session Security:** Standard cookie flags (`HttpOnly`, `SameSite=Lax`, `Secure` over HTTPS/TLS).<br>• **Cryptographic Checksums:** Pure CCITT-16 CRC recalculation (`0x1021`, `0xFFFF`) for EMVCo Dynamic QRIS. |
| **A03: Injection (SQLi / Command Injection)** | • **100% Parameterized ORM:** Zero raw SQL concatenation (`cr.execute("..." + var)`). All queries use Odoo's native ORM (`search`, `filtered`, `mapped`, `write`, `create`) executed via safe parameterized Postgres adapters. |
| **A04: Insecure Design** | • **Least Privilege Principle:** Sensitive actions (assigning NSFP pools, posting marketplace split journals, affixing Peruri e-Meterai, reconciling bank mutations) require explicit accounting group authorization (`account.group_account_manager` or `account.group_account_user`). |
| **A05: Security Misconfiguration** | • Production configurations enforce disabled `--dev` mode.<br>• Sensitive exception stack traces are sanitized from public API responses. |
| **A06: Vulnerable & Outdated Components** | • Automated dependency scanning via **GitHub Dependabot** (`.github/dependabot.yml`).<br>• Zero external C-extension binary dependencies; lightweight Python dependencies strictly pinned. |
| **A07: Identification & Authentication Failures** | • Inbound webhook controllers (`/api/v1/webhook/qris`) validate shared HMAC/API secret tokens before triggering state mutations.<br>• Native support for Odoo Two-Factor Authentication (2FA/TOTP) and session expiration. |
| **A08: Software & Data Integrity Failures** | • Complete audit chatter tracking (`tracking=True`) on critical invoice financial fields (NSFP number, e-Meterai serial, QRIS payment status).<br>• Automated GitHub Actions CI pipeline running full regression suites on every pull request. |
| **A09: Security Logging & Monitoring Failures** | • Dedicated audit logging via Python's standard `logging` module and Odoo `ir.logging`.<br>• Detailed audit trail for tax exports, marketplace settlements, and e-Meterai quota deductions. |
| **A10: Server-Side Request Forgery (SSRF) & XSS** | • **XSS Mitigation:** All QWeb PDF and HTML views strictly use auto-escaping `<t t-out="..." />` directives.<br>• **SSRF Prevention:** API connectors validate outgoing endpoints and restrict loopback/private CIDR blocks unless explicitly configured in Sandbox mode. |

---

## 🤖 Automated Security Testing & CodeQL (SAST)

Our development workflow incorporates **Automated Static Application Security Testing (SAST)**:

- **GitHub CodeQL (`.github/workflows/codeql.yml`):** Runs deep semantic Abstract Syntax Tree (AST) analysis on Python source code on every push and pull request to detect CWE vulnerabilities (SQL injection, path traversal, hardcoded secrets, unsafe deserialization).
- **Vendor Guideline Audit (`scripts/validate_apps_store.py`):** Automatically validates manifest security, licensing integrity, dependency declarations, and namespace collisions.

---

## 🚨 Vulnerability Reporting & Responsible Disclosure

We value the security research community. If you discover a potential vulnerability, security flaw, or access control weakness:

1. **Do Not File a Public Issue:** Please refrain from publishing vulnerability details in public GitHub issues, pull requests, or discussion boards.
2. **Submit a Confidential Advisory:**
   - Use [GitHub Private Vulnerability Reporting](https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite/security/advisories/new) directly on the repository.
   - Alternatively, email the Security Response Team at: **`billing@ppti.me`** with the subject `[SECURITY] Potential Vulnerability in MangoTek Financial Suite`.
3. **Report Contents:**
   - Affected module(s) and Odoo series (`18.0`, `19.0`, or `20.0`).
   - Detailed description and proof of concept (PoC) steps to reproduce.
   - Potential impact on confidentiality, integrity, or availability.
   - Suggested mitigation or patch, if available.

### Response SLA & Coordination
- **Initial Acknowledgment:** Within **24–48 hours**.
- **Triage & Reproducibility Assessment:** Within **3 business days**.
- **Hotfix Release & CVE Coordination:** Critical vulnerabilities will be patched immediately with coordinated public disclosure and appropriate credit/attribution to the reporter.

---

*Maintained by the MangoTek Security Engineering Team · Licensed under GNU LGPL-3.0*
