# parser.py
import PyPDF2
from utils import clean_text

def parse_resume(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return clean_text(text)
