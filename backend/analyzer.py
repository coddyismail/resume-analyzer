import re

# -------------------------------
# Basic Skill Database
# -------------------------------
SKILLS = [
    "python", "java", "c++", "flask", "django", "react", "node",
    "sql", "mysql", "mongodb", "machine learning", "deep learning",
    "aws", "docker", "html", "css", "javascript", "typescript",
    "express", "git", "linux", "rest api"
]

def analyze_resume(text):

    # Clean text
    t = text.lower()

    # Word count
    words = len(t.split())

    # Skills detected
    found_skills = [skill for skill in SKILLS if skill in t]

    # Email & phone extraction
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phones = re.findall(r"\+?\d[\d \-]{8,13}\d", text)

    # Fake ATS score formula
    ats_score = round((len(found_skills) / len(SKILLS)) * 100, 2)

    # Suggestions based on resume quality
    suggestions = []
    if ats_score < 40:
        suggestions.append("Add more relevant technical skills.")
    if words < 150:
        suggestions.append("Your resume looks short. Add more project details.")
    if words > 450:
        suggestions.append("Try shortening your resume for better readability.")
    if not emails:
        suggestions.append("Add a professional email address.")
    if not phones:
        suggestions.append("Add an active phone number.")

    if not suggestions:
        suggestions = ["Looks good!"]

    return {
        "ats_score": ats_score,
        "word_count": words,
        "skills": found_skills,
        "emails": emails,
        "phones": phones,
        "suggestions": suggestions
    }
