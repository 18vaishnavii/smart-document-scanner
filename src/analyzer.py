import re


SKILLS = [
    "python", "java", "c++", "html", "css", "javascript",
    "sql", "mysql", "mongodb", "django", "flask", "streamlit",
    "opencv", "numpy", "pandas", "machine learning", "data analysis",
    "git", "github", "excel", "power bi"
]


def extract_email(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return emails


def extract_phone(text):
    phones = re.findall(r"(\+?\d[\d\s-]{8,}\d)", text)
    return phones


def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill.title())

    return found_skills


def detect_document_type(text):
    text_lower = text.lower()

    if "resume" in text_lower or "education" in text_lower or "skills" in text_lower:
        return "Resume"

    if "invoice" in text_lower or "amount" in text_lower or "total" in text_lower:
        return "Invoice"

    if "certificate" in text_lower or "awarded" in text_lower:
        return "Certificate"

    if "notes" in text_lower or "chapter" in text_lower:
        return "Notes"

    return "General Document"


def calculate_resume_score(text, skills):
    score = 0
    text_lower = text.lower()

    if extract_email(text):
        score += 15

    if extract_phone(text):
        score += 15

    if len(skills) >= 3:
        score += 25
    elif len(skills) > 0:
        score += 10

    if "project" in text_lower or "projects" in text_lower:
        score += 15

    if "education" in text_lower:
        score += 10

    if "experience" in text_lower or "internship" in text_lower:
        score += 10

    if "github" in text_lower or "linkedin" in text_lower:
        score += 10

    return min(score, 100)


def get_resume_suggestions(text, skills):
    suggestions = []
    text_lower = text.lower()

    if not extract_email(text):
        suggestions.append("Add a professional email address.")

    if not extract_phone(text):
        suggestions.append("Add a phone number.")

    if len(skills) < 3:
        suggestions.append("Add more technical skills relevant to the job role.")

    if "project" not in text_lower and "projects" not in text_lower:
        suggestions.append("Add a projects section with technologies used.")

    if "github" not in text_lower:
        suggestions.append("Add your GitHub profile link.")

    if "linkedin" not in text_lower:
        suggestions.append("Add your LinkedIn profile link.")

    if not suggestions:
        suggestions.append("Resume looks well structured. Add measurable achievements if possible.")

    return suggestions


def analyze_document(text):
    document_type = detect_document_type(text)
    emails = extract_email(text)
    phones = extract_phone(text)
    skills = extract_skills(text)

    result = {
        "document_type": document_type,
        "emails": emails,
        "phones": phones,
        "skills": skills,
        "score": None,
        "suggestions": []
    }

    if document_type == "Resume":
        result["score"] = calculate_resume_score(text, skills)
        result["suggestions"] = get_resume_suggestions(text, skills)

    return result