# AI resume
AI Resume Analyzer

A Python + Streamlit tool that extracts text from a resume (including scanned/image-based PDFs via OCR) and generates a skill-gap analysis prompt to compare it against a job description.

Features
PDF text extraction — reads real, text-based PDF resumes directly
OCR fallback — automatically detects scanned or image-based PDFs (e.g. photos, WhatsApp exports) and extracts text using Tesseract OCR
Streamlit web UI — upload a resume, paste a job description, and get an auto-generated analysis prompt
Skill-gap analysis — identifies matched skills, missing skills, and improvement suggestions (via Claude)
Tech Stack
Python
Streamlit — web UI
pdfplumber — text extraction from digital PDFs
pytesseract + pdf2image — OCR for scanned/image PDFs
Tesseract OCR and Poppler — external OCR/PDF-rendering engines (not included in this repo — see setup below)
How It Works
Upload a resume PDF
The app tries direct text extraction first; if the PDF has no real text layer, it automatically falls back to OCR
Paste in a job description
The app generates a structured prompt combining both
Paste that prompt into an LLM (e.g. Claude) to get back matched skills, missing skills, and resume improvement suggestions
Setup
1. Clone the repo
bash
git clone https://github.com/bmathumitha/AI-resume-analyser.git
cd AI-resume-analyser
2. Install Python dependencies
bash
pip install streamlit pdfplumber pytesseract pdf2image pillow
3. Install external OCR tools (required for scanned PDFs)
Tesseract OCR: Windows installer
Poppler: Windows binaries

After installing, update the paths at the top of app.py and step1b_ocr_extract.py to match where you installed them:

python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\path\to\poppler\Library\bin"
4. Run the app
bash
streamlit run app.py
Project Structure
├── app.py                     # Streamlit web UI
├── step1_extract_text.py      # Standalone script: basic PDF text extraction
├── step1b_ocr_extract.py      # Standalone script: OCR-based text extraction
└── README.md
What I Learned
   Handling both text-based and scanned/image-based PDFs
   Building OCR pipelines with Tesseract and Poppler
   Creating a simple web UI with Streamlit
   Structuring prompts for reliable LLM-based analysis
   Setting up and publishing a project with Git and GitHub
Future Improvements
   Automate the analysis step by integrating an LLM API directly (currently a manual copy-paste step)
   Add ATS-style keyword matching
   Support .docx resumes
   Deploy as a hosted web app

