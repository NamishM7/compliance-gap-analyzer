# 🛡️ AI-Powered Compliance Gap Analyzer

An **AI-driven Streamlit application** that helps organizations **identify gaps** in their security policies against popular compliance frameworks such as **ISO 27001**, **NIST CSF**, and **GDPR**.

This tool uses **Natural Language Processing (NLP)** and **semantic similarity matching** to analyze uploaded documents and highlight whether each control is **Fully Covered**, **Partially Covered**, or **Not Covered**. It also provides **PDF/CSV reports** and an **interactive compliance chatbot** for quick queries.

---

## 🚀 Features

- **Multi-format document upload** — Supports PDF, DOCX, and TXT files.
- **Multiple compliance frameworks** — ISO 27001, NIST CSF, GDPR.
- **AI-based similarity scoring** — Uses `sentence-transformers` for semantic matching.
- **Coverage classification** — Fully Covered ✅ | Partially Covered 🟠 | Not Covered ❌.
- **Highlight matched sentences** from your policy.
- **Export analysis results** to CSV or PDF.
- **Interactive chatbot** for quick compliance-related queries.
- **Filter results** by coverage status.

---

## 🖥️ Tech Stack

- **Frontend & App Hosting**: [Streamlit](https://streamlit.io)
- **NLP Model**: `all-MiniLM-L6-v2` from [SentenceTransformers](https://www.sbert.net)
- **File Parsing**: `PyPDF2`, `python-docx`
- **Report Generation**: `fpdf`, `pandas`
- **Programming Language**: Python 3.8+

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/NamishM7/compliance-gap-analyzer.git
cd compliance-gap-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
