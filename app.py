import streamlit as st
import pdfplumber
import ollama
from fpdf import FPDF
import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Practical AI Builder", page_icon="🚀")

# ---------------- HEADER ----------------
st.title("🚀 Practical AI Builder – AI Resume Analyzer")
st.write("Upload your resume and get a professional AI-powered report")

# ---------------- INPUTS ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description (optional)")

# ---------------- EXTRACT TEXT ----------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ---------------- AI ANALYSIS ----------------
def analyze_resume(resume_text, job_desc):
    prompt = f"""
You are an expert HR AI.

Analyze the resume and provide structured output:

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Return clearly formatted:

Resume Score: /100
Job Match: %
Strengths:
Weaknesses:
Improvements:
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# ---------------- PREMIUM PDF REPORT ----------------
def create_pdf(report_text):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 18)
    pdf.cell(200, 10, "AI Resume Analysis Report", ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(200, 8, f"Generated on: {datetime.date.today()}", ln=True, align="C")

    pdf.ln(10)

    # Content
    lines = report_text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if any(keyword in line.lower() for keyword in ["score", "match", "strength", "weakness", "improvement"]):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, line, ln=True)
        else:
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 6, line)

    file_path = "AI_Resume_Premium_Report.pdf"
    pdf.output(file_path)

    return file_path

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.text_area("Extracted Resume", resume_text, height=250)

    if st.button("🚀 Analyze Resume"):
        with st.spinner("AI is analyzing your resume..."):
            result = analyze_resume(resume_text, job_desc)

        st.subheader("📊 AI Report")
        st.write(result)

        pdf_file = create_pdf(result)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "⬇️ Download Premium Report",
                f,
                file_name="AI_Resume_Report.pdf"
            )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Built with ❤️ by Practical AI Builder | Python + AI + Streamlit")