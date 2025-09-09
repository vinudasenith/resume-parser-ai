import re
import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_ats_compatibility(parsed_data: dict, text: str) -> dict:
    score = 0
    total_score = 100 
    messages={} 


    # Contact
    if parsed_data.get("email"):
        score += 10
        messages["email"]="Success:Email detected"
    else:
        messages["email"]="Failure:Email not detected"



    if parsed_data.get("phone"):
        score += 5
        messages["phone"]="Success:Phone number detected"
    else:
        messages["phone"]="Failure:Phone number not detected"



    if parsed_data.get("links") and parsed_data["links"].get("linkedin"):
        score += 5
        messages["linkedin"]="Success:LinkedIn profile detected"
    else:
        messages["linkedin"]="Failure:LinkedIn profile not detected"


    # Section Coverage
    if parsed_data.get("education"):
        score += 10


    if parsed_data.get("skills") or parsed_data.get("technologies"):
        score += 10


    # Experience & Projects
    has_experience = bool(parsed_data.get("experience"))
    has_projects = bool(parsed_data.get("projects"))

    if has_experience and has_projects:
        score += 10
    elif has_experience:
        score += 5
    elif has_projects:
        score += 5


    # Content Quality
    word_count = parsed_data.get("word_count", 0)
    if 200 <= word_count <= 1300:  # increased upper limit
        score += 10
        messages["Word count"]="Success:Word count within range"
    else:
        messages["Word count"]="Failure:Word count out of range"


    # Detect bullets
    if re.search(r"(•|- |\d+\.)", text):
        score += 5
        messages["bullets"]="Success:Bullets detected"
    else:
        messages["bullets"]="Failure:Bullets not detected"


    # Action verbs
    action_verbs = ["developed", "managed", "designed", "led", "created", "built", "implemented"]
    if any(verb in text.lower() for verb in action_verbs):
        score += 5


    # crude spelling check 
    tokens = [t.text for t in nlp(text) if t.is_alpha]
    misspelled = [w for w in tokens if not nlp.vocab.has_vector(w.lower())]
    if len(misspelled) < 10:
        score += 10
        messages["misspelled"]="Success:No misspelled words"
    else:
        messages["misspelled"]="Failure:Misspelled words detected"



    # Formatting 
    if not re.search(r"(image|figure|chart|table)", text, re.IGNORECASE):
        score += 5  
        messages["images"]="Success:No unnecessary images detected"
    else:
        messages["images"]="Failure:Images detected (not ATS-friendly)"



    if not re.search(r"\|", text) and not re.search(r"\t{2,}", text):
        score += 5  
        messages["tabs"]="Success:No tabular formatting detected"
    else:
        messages["tabs"]="Failure:Tabs or tables detected"



    # Check for required 
    required_headers_options = {
        "Experience & Projects": ["WORK EXPERIENCE", "EXPERIENCES,", "PROJECTS"],
        "Education": ["EDUCATION", "ACADEMIC QUALIFICATIONS", "ACADEMIC BACKGROUND"],
        "Skills": ["SKILLS", "TECHNOLOGIES AND TOOLS"]
    }

    for friendly_name, variants in required_headers_options.items():
        if any(v in text.upper() for v in variants):
            score += 10 / len(required_headers_options)

    # Normalize to percentage
    ats_percentage = round((score / total_score) * 100)
    return {"ats_percentage": ats_percentage, "messages": messages}
