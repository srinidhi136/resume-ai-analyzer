import streamlit as st
import pdfplumber
import requests
from fpdf import FPDF
import datetime

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🚀",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("🚀 ResumeAI Pro")

    st.markdown("---")

    st.subheader("Features")
    st.write("✅ Resume Analysis")
    st.write("✅ ATS Scoring")
    st.write("✅ Job Matching")
    st.write("✅ PDF Reports")

    st.markdown("---")

    st.subheader("About")
    st.write("AI Resume Analyzer built with Streamlit + Groq AI")

    st.markdown("---")

    st.caption("Version 1.0")

# =========================
# HEADER
# =========================

st.title("🚀 ResumeAI Pro")

st.markdown("### AI Resume Analyzer & ATS Optimizer")

st.info("Upload your resume and optionally add a job description for better results.")

# =========================
# EXTRACT TEXT
# =========================

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# =========================
# AI FUNCTION (GROQ)
# =========================

def analyze_resume(resume_text, job_desc):

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        return "ERROR: Missing GROQ_API_KEY in Streamlit Secrets"

    prompt = f"""
You are an expert HR AI.

Analyze this resume:

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Return:

Resume Score: X/100

Job Match: X%

Strengths:
- point

Weaknesses:
- point

Improvements:
- point
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return f"API ERROR {response.status_code}: {response.text}"

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"ERROR: {str(e)}"

# =========================
# PDF GENERATOR
# =========================

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ResumeAI Pro Report", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 10, f"Generated: {datetime.date.today()}", ln=True)

    pdf.ln(5)

    for line in text.split("\n"):
        pdf.multi_cell(0, 7, line)

    file_name = "resume_report.pdf"
    pdf.output(file_name)

    return file_name

# =========================
# UI INPUTS
# =========================

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description (Optional)", height=150)

# =========================
# MAIN LOGIC
# =========================

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Preview")
    st.text_area("Extracted Text", resume_text, height=250)

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text, job_desc)

        st.success("Analysis Complete")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Status", "Done")

        with col2:
            st.metric("Engine", "Groq AI")

        with col3:
            st.metric("Output", "Ready")

        st.subheader("AI Report")
        st.write(result)

        pdf_file = create_pdf(result)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "Download PDF Report",
                f,
                file_name="ResumeAI_Report.pdf",
                mime="application/pdf"
            )

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption("Built with Streamlit + Groq AI 🚀")