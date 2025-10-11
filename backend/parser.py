import pdfplumber
import docx

def parse_resume(file):
    filename = file.filename.lower()
    text = ""

    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")

    else:
        text = ""

    return text.strip()
