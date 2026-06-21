import streamlit as st
import pdfplumber
import requests
from fpdf import FPDF
import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Practical AI Builder",
    page_icon="🚀",
    layout="wide"
)

# ---------------- HEADER ----------------

st.title("🚀 Practical AI Builder - AI Resume Analyzer")
st.markdown(
    "Upload your resume and receive an AI-powered professional review."
)

# ---------------- API KEY ----------------

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_desc = st.text_area(
    "Paste Job Description (Optional)",
    height=150
)

# ---------------- PDF EXTRACTION ----------------

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
You are an expert HR consultant.

Analyze the following resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Provide a professional report using EXACTLY this structure:

Resume Score: X/100

Job Match: X%

Strengths:
- item
- item

Weaknesses:
- item
- item

Improvements:
- item
- item
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]

# ---------------- PDF REPORT ----------------

def create_pdf(report_text):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(
        0,
        12,
        "AI Resume Analysis Report",
        ln=True,
        align="C"
    )

    pdf.set_font("Arial", "", 11)

    pdf.cell(
        0,
        8,
        f"Generated: {datetime.date.today()}",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    lines = report_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if any(
            keyword in line.lower()
            for keyword in [
                "resume score",
                "job match",
                "strengths",
                "weaknesses",
                "improvements"
            ]
        ):
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 8, line)

        else:
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 7, line)

    file_path = "AI_Resume_Report.pdf"

    pdf.output(file_path)

    return file_path

# ---------------- MAIN APP ----------------

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume",
        resume_text,
        height=250
    )

    if st.button("🚀 Analyze Resume"):

        with st.spinner("Analyzing resume..."):

            result = analyze_resume(
                resume_text,
                job_desc
            )

        st.subheader("📊 AI Report")

        st.markdown(result)

        pdf_file = create_pdf(result)

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name="AI_Resume_Report.pdf",
                mime="application/pdf"
            )

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Built by Practical AI Builder | Python + Streamlit + Groq AI"
)