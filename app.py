```python
import streamlit as st
import pdfplumber
import requests
from fpdf import FPDF
import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🚀",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🚀 ResumeAI Pro")

    st.markdown("---")

    st.subheader("Features")

    st.write("✅ Resume Analysis")
    st.write("✅ ATS Suggestions")
    st.write("✅ Job Match Review")
    st.write("✅ PDF Report Export")

    st.markdown("---")

    st.subheader("About")

    st.write(
        "AI-powered resume analysis tool built using "
        "Streamlit + Groq AI."
    )

    st.markdown("---")

    st.caption("Version 1.0")

# =====================================
# HEADER
# =====================================

st.title("🚀 ResumeAI Pro")

st.markdown(
    """
### AI-Powered Resume Analysis & ATS Optimization

Upload your resume and receive:

- ATS Resume Score
- Job Match Percentage
- Strengths & Weaknesses
- Improvement Suggestions
- Downloadable PDF Report
"""
)

st.info(
    "Upload your resume PDF and optionally paste a job description for a more accurate analysis."
)

# =====================================
# PDF TEXT EXTRACTION
# =====================================

def extract_text(uploaded_file):

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

# =====================================
# AI ANALYSIS
# =====================================

def analyze_resume(resume_text, job_desc):

    try:
        api_key = st.secrets["GROQ_API_KEY"]

    except:
        return "❌ GROQ_API_KEY not found in Streamlit Secrets."

    prompt = f"""
You are an expert HR consultant.

Analyze this resume professionally.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

Provide exactly:

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
API Error

Status Code: {response.status_code}

{response.text}
"""

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"

# =====================================
# PDF GENERATOR
# =====================================

def create_pdf(report_text):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", "B", 18)

    pdf.cell(
        0,
        12,
        "ResumeAI Pro Analysis Report",
        ln=True,
        align="C"
    )

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)

    pdf.cell(
        0,
        8,
        f"Generated: {datetime.date.today()}",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font("Arial", "", 11)

    for line in report_text.split("\n"):

        pdf.multi_cell(
            0,
            7,
            line
        )

    file_name = "ResumeAI_Report.pdf"

    pdf.output(file_name)

    return file_name

# =====================================
# INPUTS
# =====================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume PDF",
    type=["pdf"]
)

job_desc = st.text_area(
    "💼 Paste Job Description (Optional)",
    height=180
)

# =====================================
# PROCESSING
# =====================================

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=250
    )

    if st.button("🚀 Analyze Resume"):

        with st.spinner("Analyzing resume..."):

            report = analyze_resume(
                resume_text,
                job_desc
            )

        st.success("✅ Analysis Completed")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Status",
                "Analyzed"
            )

        with col2:
            st.metric(
                "AI Engine",
                "Groq"
            )

        with col3:
            st.metric(
                "Report",
                "Ready"
            )

        st.markdown("---")

        st.subheader("📊 Analysis Report")

        st.write(report)

        pdf_file = create_pdf(report)

        with open(pdf_file, "rb") as file:

            st.download_button(
                label="⬇ Download PDF Report",
                data=file,
                file_name="ResumeAI_Report.pdf",
                mime="application/pdf"
            )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "Built by Practical AI Builder | Streamlit + Groq AI"
)
```
