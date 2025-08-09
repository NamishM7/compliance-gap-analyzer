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
```
---

## 📂 Project Structure
```
compliance-gap-analyzer/
│
├── app.py                      # Main Streamlit app
├── requirements.txt            # Dependencies
├── data/                       # JSON control definitions for each framework
│   ├── iso27001_controls.json
│   ├── nist_csrf_controls.json
│   └── gdpr_controls.json
├── docs/                       # (Optional) screenshots / additional docs
│   ├── compliance_results.png
│   └── chatbot.png
└── README.md
```
---



## 🔮 How It Works

1. **Upload your policy document** (PDF, DOCX, or TXT).
2. The app **extracts the text**.
3. Each control requirement from the selected framework is **encoded into embeddings**.
4. Your policy text is also encoded and compared using **cosine similarity**.
5. The similarity score determines coverage status.
6. Results are displayed with **color-coded highlights** and can be **exported**.

---

## 📜 Example Use Cases

- **CISO teams** verifying compliance readiness.
- **Security auditors** assessing policy coverage.
- **Startups & SMBs** preparing for certification.
- **Students & researchers** learning about NLP in compliance.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open an issue or submit a pull request.

---

## 📄 License

MIT License — free to use and modify.

