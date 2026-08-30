"""
Resume Analyzer - Simple Web UI (no API key needed)

This app lets you:
1. Upload a resume (PDF)
2. Paste a job description
3. Get a ready-made prompt to paste into claude.ai
4. Paste Claude's answer back in to see it displayed nicely

Before running, install:
    pip install streamlit pdfplumber pytesseract pdf2image pillow

Run with:
    streamlit run app.py

(Note: streamlit run, NOT python app.py - Streamlit apps are started
differently from normal scripts.)
"""

import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os

# --- Your machine's OCR tool paths (only used if the PDF has no text layer) ---
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\surya b\Desktop\AI resume\poppler-26.02.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
# --------------------------------------------------------------------------------


def extract_text_normal(pdf_path):
    """Try extracting real text first (fast, works for text-based PDFs)."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_ocr(pdf_path):
    """Fallback: OCR the PDF (for scanned/image-based PDFs)."""
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    text = ""
    for image in pages:
        text += pytesseract.image_to_string(image) + "\n"
    return text


def extract_resume_text(pdf_path):
    """Try normal extraction, fall back to OCR if no text was found."""
    text = extract_text_normal(pdf_path)
    if len(text.strip()) < 20:  # basically empty -> probably a scanned PDF
        st.info("No text layer found — running OCR instead (this can take a few seconds)...")
        text = extract_text_ocr(pdf_path)
    return text


def build_prompt(resume_text, job_description):
    return f"""Here is a resume:

{resume_text}

Here is a job description I'm targeting:

{job_description}

Please analyze this and return:
1. Skills from the resume that match the job
2. Important skills required by the job but missing from the resume
3. 3 specific, actionable suggestions to improve this resume for this role"""


# ---------------- UI ----------------

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")
st.caption("Upload a resume, paste a job description, and get a skill-gap analysis.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload your resume")
    uploaded_file = st.file_uploader("Choose a PDF resume", type=["pdf"])

    resume_text = ""
    if uploaded_file is not None:
        # Save the uploaded file temporarily so pdfplumber/OCR can open it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with st.spinner("Extracting text..."):
            resume_text = extract_resume_text(tmp_path)

        os.remove(tmp_path)

        if resume_text.strip():
            st.success(f"Extracted {len(resume_text)} characters.")
            with st.expander("View extracted resume text"):
                st.text(resume_text)
        else:
            st.error("Couldn't extract any text from this PDF.")

with col2:
    st.subheader("2. Paste the job description")
    job_description = st.text_area("Job description", height=250)

st.divider()

if resume_text and job_description:
    st.subheader("3. Copy this prompt into claude.ai")
    prompt = build_prompt(resume_text, job_description)
    st.text_area("Prompt to copy", prompt, height=200)
    st.caption("Copy the text above, paste it into a new chat at claude.ai, and copy Claude's reply back below.")

    st.subheader("4. Paste Claude's response here to view it")
    response = st.text_area("Claude's response", height=200)
    if response:
        st.subheader("Results")
        st.markdown(response)
else:
    st.info("Upload a resume and paste a job description to generate your analysis prompt.")
