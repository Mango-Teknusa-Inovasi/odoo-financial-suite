# Contributing to Odoo Financial Suite

Thank you for your interest in contributing to **Odoo Financial Suite**! Contributions from the community help make this toolkit better for businesses across Indonesia.

---

## 🛠️ Development Workflow

### 1. Branching Strategy

* `main`: Production-ready releases only.
* `dev`: Integration branch for new features and bug fixes.
* Feature branches: Follow the naming convention `feature/<module-name>-<short-description>` or `fix/<module-name>-<issue-id>`.

### 2. Odoo Coding Standards

When authoring code for this suite, adhere strictly to the following conventions:
* **Clean Model Inheritance:** Always extend models using `_inherit`. Avoid modifying standard Odoo fields destructively.
* **PEP 8 Compliance:** All Python code must be clean, readable, and properly formatted according to PEP 8 standards (4-space indentation).
* **Security Definitions:** Every newly declared model (`models.Model`) must have an explicit access rule in `security/ir.model.access.csv`.
* **XML Architecture:** Keep views organized in distinct directories (`views/`, `data/`, `security/`, `reports/`). Use semantic IDs prefixed with the module name.
* **Internationalization:** Enclose user-facing strings in `_()` translation markers.

---

## 📝 Commit Convention

Commit messages should be concise and descriptive, following conventional commit syntax:
* `feat(module): add new functionality`
* `fix(module): resolve calculation defect`
* `docs(readme): improve documentation`
* `refactor(module): clean up business logic`

---

## 🚀 Submitting a Pull Request (PR)

1. Fork the repository and create your branch from `main` or `dev`.
2. Test your changes locally in an active Odoo instance to ensure zero traceback warnings.
3. Commit your changes with descriptive messages.
4. Submit a Pull Request targeting `main`. Provide a clear summary of what your PR accomplishes and how it was tested.
