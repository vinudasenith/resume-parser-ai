from transformers import pipeline

# Load model once (global)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def is_resume_ai(text: str) -> bool:

    candidate_labels = ["resume", "cv", "job application", "not a resume"]
    snippet = text[:3000]  
    result = classifier(snippet, candidate_labels)

    # Pick the label with highest score
    best_label = result["labels"][0]
    best_score = result["scores"][0]

    print("AI Classification:", best_label, best_score)

    return best_label in ["resume", "cv", "job application"] and best_score > 0.6

def has_resume_keywords(text: str) -> bool:

    sections = ["WORK EXPERIENCE", "ACADEMIC QUALIFICATIONS", "PROJECTS", 
                "TECHNOLOGIES AND TOOLS", "CERTIFICATIONS"]
    
    text_upper = text.upper()
    for sec in sections:
        if sec in text_upper:
            return True
    return False

def is_resume_ai_combined(text: str) -> bool:

    ai_check = is_resume_ai(text)
    keyword_check = has_resume_keywords(text)
    return ai_check or keyword_check 

