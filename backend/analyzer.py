# analyzer.py
from backend.utils import clean_text, extract_emails, extract_phone_numbers, word_count

def analyze_resume(text: str):
    text = clean_text(text)
    emails = extract_emails(text)
    phones = extract_phone_numbers(text)
    words = word_count(text)
    
    return {
        "word_count": words,
        "emails": emails,
        "phone_numbers": phones
    }
