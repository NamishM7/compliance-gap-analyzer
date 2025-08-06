# ----------------------------
# 1. Import Libraries
# ----------------------------
import os
import json
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from sentence_transformers import SentenceTransformer, util
import numpy as np
import re
from fpdf import FPDF
import pandas as pd

# st.title("AI-Powered Compliance Gap Analyzer")
# st.write("Welcome to your compliance gap analyzer app!")

# ----------------------------
# 2. Load Controls
# ----------------------------
def load_controls(framework):
    # Map framework names to file paths
    framework_files = {
        "ISO 27001": "iso27001_controls.json",
        "NIST CSF": "nist_csrf_controls.json",
        "GDPR": "gdpr_controls.json"
    }

    # Get the corresponding file name
    file_name = framework_files.get(framework)

    if not file_name:
        raise ValueError(f"Unsupported framework: {framework}")

    # Load the JSON file
    with open(f"data/{file_name}") as f:
        return json.load(f)

# ----------------------------
# 3. Extract Text from Files
# ----------------------------
def extract_text(file):
    name, ext = os.path.splitext(file.name)
    if ext == ".pdf":
        pdf_reader = PdfReader(file)
        text = " ".join(page.extract_text() for page in pdf_reader.pages)
    elif ext == ".docx":
        doc = Document(file)
        text = " ".join(paragraph.text for paragraph in doc.paragraphs)
    elif ext == ".txt":
        text = str(file.read(), 'utf-8')
    else:
        text = ""

    # Debugging: Print extracted text
    print(f"Extracted Text: {text}")
    return text

# ----------------------------
# 4. Semantic Matching Logic
# ----------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')

def analyze_compliance(policy_text, controls, threshold=0.55):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    results = []

    for control in controls:
        req = control['description']
        req_embedding = model.encode(req, convert_to_tensor=True)
        policy_embedding = model.encode(policy_text, convert_to_tensor=True)

        similarity = util.cos_sim(req_embedding, policy_embedding).item()

        status = "Fully Covered" if similarity > threshold + 0.1 \
            else "Partially Covered" if similarity > threshold \
            else "Not Covered"

        match_sentence = highlight_matches(policy_text, req, model)

        results.append({
            "control_id": control["control_id"],
            "title": control["title"],
            "similarity": round(similarity, 2),
            "status": status,
            "matched_sentence": match_sentence
        })

    # Debugging: Print results to console
    print("Results:", results)
    return sorted(results, key=lambda x: x["similarity"], reverse=True)

# ----------------------------
# 5. Highlight Matching Sentences
# ----------------------------
def highlight_matches(text, query, model, threshold=0.5):
    sentences = text.split('.')
    best_match = ""
    max_score = 0

    query_emb = model.encode(query, convert_to_tensor=True)

    for sent in sentences:
        if len(sent.strip()) < 5:
            continue
        sent_emb = model.encode(sent, convert_to_tensor=True)
        score = util.cos_sim(query_emb, sent_emb).item()
        if score > max_score and score > threshold:
            max_score = score
            best_match = sent.strip()

    return best_match if max_score > threshold else None

# ----------------------------
# 6. Export Functions
# ----------------------------
def export_to_csv(results):
    df = pd.DataFrame(results)
    return df.to_csv(index=False).encode('utf-8')



from fpdf import FPDF

def export_to_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, txt="Compliance Gap Analysis Report", ln=True, align='C')
    pdf.ln(10)

    for res in results:
        pdf.cell(200, 8, txt=f"Control {res['control_id']}: {res['title']}", ln=True)
        
        # Strip emoji before exporting
        status_text = res['status'].split(" ", 1)[1] if " " in res['status'] else res['status']
        pdf.cell(200, 8, txt=f"Status: {status_text}", ln=True)
        
        pdf.cell(200, 8, txt=f"Similarity Score: {res['similarity']}", ln=True)
        pdf.cell(200, 8, txt=f"Matched Sentence: {res.get('matched_sentence', 'None')}", ln=True)
        pdf.ln(6)

    return bytes(pdf.output(dest='S'))

# ----------------------------
# 7. Chatbot Assistant
# ----------------------------
def chatbot(question, results):
    keywords = {
        "password complexity": "A.9.2.3",
        "segregation of duties": "A.6.1.2",
        "information security policy": "A.5.1",
        "encryption": "A.13.1.1",
        "data classification": "A.8.2.1"
    }

    question = question.lower()
    for key in keywords:
        if key in question:
            control_id = keywords[key]
            for res in results:
                if res["control_id"] == control_id:
                    return f"""
                    Control ID: {res['control_id']}
                    Title: {res['title']}
                    Status: {res['status']}
                    Matched Sentence: {res['matched_sentence']}
                    """
    return "I couldn't understand your question."

# ----------------------------
# 8. Main Streamlit App
# ----------------------------
def main():
    st.set_page_config(page_title="🛡️ AI Compliance Gap Analyzer", layout="wide")
    st.title("🛡️ AI-Powered Compliance Gap Analyzer")
    st.markdown("Upload your organization's security policy and check alignment with selected frameworks.")

    # Sidebar: Framework Selection
    st.sidebar.header("Framework Selection")
    framework = st.sidebar.selectbox(
        "Choose Compliance Framework",
        ["ISO 27001", "NIST CSF", "GDPR"]
    )
    controls = load_controls(framework)

    # Upload File
    uploaded_file = st.file_uploader("Upload Policy (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file:
        with st.spinner("Analyzing document..."):
            policy_text = extract_text(uploaded_file)
            results = analyze_compliance(policy_text, controls)

        st.success("Analysis Complete!")
        st.write("### 🔍 Compliance Results:")

        # Filter Options
        st.sidebar.subheader("Filter Results")
        filter_status = st.sidebar.multiselect(
    "Show Controls With Status",
    ["Fully Covered", "Partially Covered", "Not Covered"],
    default=["Fully Covered", "Partially Covered", "Not Covered"]
)

        filtered_results = [res for res in results if res["status"] in filter_status]

        if filtered_results:
            for res in filtered_results:
                color = "green" if res["status"] == "Fully Covered" \
            else "orange" if res["status"] == "Partially Covered" else "red"
                st.markdown(f"""
             <div style="background-color:#f0f0f0;padding:10px;border-left:5px solid {color};margin-bottom:10px;">
                <strong>Control {res['control_id']}: {res['title']}</strong><br/>
                - Status: <span style="color:{color}">{res['status']}</span><br/>
                - Similarity Score: <code>{res['similarity']}</code><br/>
                - Matched Sentence: <em>"{res['matched_sentence'] or 'None'}"</em>
            </div>
        """, unsafe_allow_html=True)
        else:
                st.warning("No results match the selected filters.")

                col1, col2 = st.columns(2)
                with col1:
                    csv = export_to_csv(results)
                    st.download_button("📥 Download CSV", data=csv, file_name="compliance_report.csv", mime="text/csv")
                with col2:
                    pdf = export_to_pdf(results)
                    st.download_button("📄 Download PDF", data=pdf, file_name="compliance_report.pdf", mime="application/pdf")

        st.markdown("---")
        st.subheader("🤖 Compliance Chatbot Assistant")
        question = st.text_input("Ask a compliance question (e.g., Is password complexity covered?)")

        if question:
            response = chatbot(question, results)
            st.code(response)

if __name__ == "__main__":
    main()