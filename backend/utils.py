import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9@.\s+-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_emails(text: str):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

def extract_phone_numbers(text: str):
    return re.findall(
        r"(\+?\d{1,3}[-.\s]?\d{3,5}[-.\s]?\d{3,5}[-.\s]?\d{2,4})",
        text
    )

def word_count(text: str) -> int:
    return len(text.split())
