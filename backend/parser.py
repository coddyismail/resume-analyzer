import pdfplumber
from docx import Document


def parse_resume(file):
    filename = file.filename.lower()
    text = ""

    # ---- PDF ----
    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    # ---- DOCX ----
    elif filename.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"

    # ---- TXT ----
    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")

    # ---- Unsupported Format ----
    else:
        text = ""

    return text.strip()
