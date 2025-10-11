from utils import clean_text, extract_emails, extract_phone_numbers, word_count

# Example skill keywords (expand as needed)
SKILLS = [
    "python", "java", "c++", "flask", "django", "react", "node", "sql",
    "machine learning", "deep learning", "data analysis", "aws", "docker"
]

def analyze_resume(text):
    text_clean = clean_text(text)

    found_skills = [skill for skill in SKILLS if skill in text_clean]
    score = (len(found_skills) / len(SKILLS)) * 100

    result = {
        "resume_length": word_count(text),
        "emails": extract_emails(text),
        "phone_numbers": extract_phone_numbers(text),
        "skills_found": found_skills,
        "ats_score": round(score, 2),
        "suggestions": []
    }

    if score < 50:
        result["suggestions"].append("Add more technical skills relevant to jobs.")
    if word_count(text) < 200:
        result["suggestions"].append("Expand resume with more details and achievements.")
    
    return result
