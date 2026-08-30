"""
Step 1b: Extract text from a scanned/image-based PDF using OCR.
"""

import pytesseract
from pdf2image import convert_from_path

RESUME_PATH = "resume.pdf"

# --- Your machine's paths ---
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\surya b\Desktop\AI resume\poppler-26.02.0\Library\bin"
# -----------------------------

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_with_ocr(path):
    print("Converting PDF pages to images...")
    pages = convert_from_path(path, poppler_path=POPPLER_PATH)

    full_text = ""
    for page_number, image in enumerate(pages, start=1):
        print(f"Running OCR on page {page_number}...")
        page_text = pytesseract.image_to_string(image)
        full_text += page_text + "\n"

    return full_text


if __name__ == "__main__":
    text = extract_text_with_ocr(RESUME_PATH)
    print("----- EXTRACTED TEXT -----")
    print(text)
    print("----- END -----")
    print(f"\nTotal characters extracted: {len(text)}")