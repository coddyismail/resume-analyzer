# analyzer.py
from utils import extract_emails, extract_phone_numbers, word_count

def analyze_resume(text):
    emails = extract_emails(text)
    phones = extract_phone_numbers(text)
    words = word_count(text)

    score = 0
    keywords = ["python", "javascript", "experience", "projects", "react", "node", "sql"]

    matched = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]

    score = len(matched) * 10

    return {
        "score": score,
        "word_count": words,
        "emails": emails,
        "phones": phones,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
