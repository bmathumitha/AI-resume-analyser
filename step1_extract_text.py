import pdfplumber
 
RESUME_PATH = "resume.pdf"  # <-- change this to your file's name
 
 
def extract_text_from_pdf(path):
    """Reads a PDF file and returns all its text as one string."""
    full_text = ""
 
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
            else:
                print(f"Warning: no text found on page {page_number}")
 
    return full_text
 
 
if __name__ == "__main__":
    text = extract_text_from_pdf(RESUME_PATH)
    print("----- EXTRACTED TEXT -----")
    print(text)
    print("----- END -----")
    print(f"\nTotal characters extracted: {len(text)}")