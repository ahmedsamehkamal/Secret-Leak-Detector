# 🔍 Code Secret & PII Security Scanner v2.0 Pro

> [!CAUTION]
> **LEGAL & ETHICAL USE WARNING / تحذير قانوني وأخلاقي:**
> This tool is developed strictly for **educational purposes** and **defensive security auditing** of your own source code. Scanning, analyzing, or extracting data from files, repositories, or systems belonging to third parties without explicit written authorization is strictly prohibited and illegal. The author assumes **no liability** for any misuse or damage caused by this software.
>
> **تنبيه هام:** هذه الأداة مخصصة للأغراض التعليمية وفحص أكوادك البرمجية الخاصة فقط قبل نشرها. يُمنع منعاً باتاً استخدامها لفحص ملفات أو أنظمة الغير دون إذن مسبق، ومُطوّر الأداة غير مسؤول عن أي استخدام غير قانوني.

---

A lightweight Full-Stack **Data Loss Prevention (DLP)** & **Secret Scanning** tool built with **Python** and a modern **HTML/CSS/JS** dashboard. Designed to help developers and security analysts scan source code files for hardcoded credentials, API keys, and sensitive PII before pushing to public repositories.

## ✨ Key Features
* **Direct File Upload:** Supports uploading `.py`, `.js`, `.html`, and `.txt` source files directly from the browser.
* **Exact Line-Number Pinpointing:** Identifies the exact line number (`Line X`) where each leaked secret is located.
* **Multi-Pattern Detection:** Detects hardcoded passwords, Stripe/API keys, GitHub Personal Access Tokens (`ghp_`), email addresses, and internal IP addresses.
* **One-Click Audit Reporting:** Exports a clean `.txt` security audit report directly from the web interface.

## 🚀 How to Run Locally
1. Ensure Python 3 is installed on your machine.
2. Run the local scanner server:
   ```bash
   python secret_scanner.py
   ```
3. Open your browser and navigate to: `http://localhost:9001`

## 👨‍💻 Author
**Business Information Systems (BIS) Graduate | Frontend Developer & Web Security Enthusiast**
