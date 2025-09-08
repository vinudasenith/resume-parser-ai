import re
import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_ats_compatibility(parsed_data: dict, text: str) -> int:
    score = 0
    total_score = 100  


    # Contact
    if parsed_data.get("email"):
        score += 10
    if parsed_data.get("phone"):
        score += 5
    if parsed_data["links"].get("linkedin"):
        score += 5


    # Section Coverage
    if parsed_data.get("education"):
        score += 10
    if parsed_data.get("skills") or parsed_data.get("technologies"):
        score += 10
    if parsed_data.get("experience") or parsed_data.get("projects"):
        score += 10


    # Content Quality
    word_count = parsed_data.get("word_count", 0)
    if 200 <= word_count <= 1300:  # increased upper limit
        score += 10


    # Detect bullets
    if re.search(r"(•|- |\d+\.)", text):
        score += 5


    # Action verbs
    action_verbs = ["developed", "managed", "designed", "led", "created", "built", "implemented"]
    if any(verb in text.lower() for verb in action_verbs):
        score += 5


    # crude spelling check 
    tokens = [t.text for t in nlp(text) if t.is_alpha]
    misspelled = [w for w in tokens if not nlp.vocab.has_vector(w.lower())]
    if len(misspelled) < 10:
        score += 10


    # Formatting 
    if not re.search(r"(image|figure|chart|table)", text, re.IGNORECASE):
        score += 5  



    if not re.search(r"\|", text) and not re.search(r"\t{2,}", text):
        score += 5  



    # Check for required 
    required_headers_options = {
        "EXPERIENCE_PROJECTS": ["WORK EXPERIENCE", "EXPERIENCES,", "PROJECTS"],
        "EDUCATION": ["EDUCATION", "ACADEMIC QUALIFICATIONS", "ACADEMIC BACKGROUND"],
        "SKILLS": ["SKILLS", "TECHNOLOGIES AND TOOLS"]
    }
    

    for variants in required_headers_options.values():
        if any(v in text.upper() for v in variants):
            score += 10 / len(required_headers_options)  

    # Normalize to percentage
    ats_percentage = round((score / total_score) * 100)
    return ats_percentage
