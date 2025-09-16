from transformers import pipeline

# Load model once (global)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


# Check if text looks like a resume
def is_resume_ai(text: str) -> bool:

    candidate_labels = ["resume", "cv", "curriculum vitae", "job application","career profile", "professional profile", "not a resume"]

    snippet = text[:3000] + text[-3000:]   
    result = classifier(snippet, candidate_labels)

    # Pick the label with highest score
    best_label = result["labels"][0]
    best_score = result["scores"][0]

    print("AI Classification:", best_label, best_score)

    return best_label in ["resume", "cv", "curriculum vitae", "job application"] and best_score > 0.6


# Check if text contains resume keywords
def has_resume_keywords(text: str) -> bool:

    keywords = ["WORK EXPERIENCE", "EXPERIENCES", "EDUCATION", "ACADEMIC QUALIFICATIONS","ACADEMIC BACKGROUND", "PROJECTS","SKILLS", "TECHNOLOGIES AND TOOLS","ACHIEVEMENTS", "CERTIFICATIONS", "PUBLICATIONS", "AWARDS"]
    
    text_upper = text.upper()
    hits = sum(1 for kw in keywords if kw in text_upper)
    return hits >= 3


def is_resume_ai_combined(text: str) -> bool:

    ai_check = is_resume_ai(text)
    keyword_check = has_resume_keywords(text)
    return ai_check or keyword_check 

