import streamlit as st
import pdfplumber
import requests
from fpdf import FPDF
import datetime

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Resume Analyzer")
st.write("Upload a resume and get an AI-powered review.")

# -------------------------
# PDF TEXT EXTRACTION
# -------------------------

def extract_text(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

# -------------------------
# GROQ ANALYSIS
# -------------------------

def analyze_resume(resume_text, job_desc):

    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        return "ERROR: GROQ_API_KEY not found in Streamlit Secrets."

    prompt = f"""
You are an expert HR consultant.

Analyze this resume.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Return exactly:

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

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"""
API ERROR

Status Code: {response.status_code}

Response:
{response.text}
"""

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Exception: {str(e)}"

# -------------------------
# PDF REPORT
# -------------------------

def create_pdf(report_text):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(
        0,
        10,
        "AI Resume Analysis Report",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    pdf.cell(
        0,
        8,
        f"Generated on {datetime.date.today()}",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 11)

    for line in report_text.split("\n"):
        pdf.multi_cell(0, 6, line)

    file_name = "resume_report.pdf"

    pdf.output(file_name)

    return file_name

# -------------------------
# UI
# -------------------------

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_desc = st.text_area(
    "Paste Job Description (Optional)",
    height=150
)

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Preview")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=250
    )

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing..."):

            report = analyze_resume(
                resume_text,
                job_desc
            )

        st.subheader("Analysis Report")

        st.write(report)

        pdf_file = create_pdf(report)

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="AI_Resume_Report.pdf",
                mime="application/pdf"
            )

st.markdown("---")
st.caption("Built with Streamlit + Groq AI")