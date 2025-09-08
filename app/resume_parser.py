import io
import re
import pdfplumber
import spacy

#load spacy NLP model
nlp=spacy.load("en_core_web_sm")

#extract text from pdf
def extract_text_from_pdf(pdf_bytes:bytes) -> str:
    text= ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text=page.extract_text()
                if page_text:
                    text+=page_text +"\n"
    except Exception as e:
        print(e)
    return text


# extract email 
def extract_email(text):
    match =re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if match:
        return match.group(0).strip()
    return None


# extract links
def extract_links(text):
    links = {}

    # LinkedIn
    linkedin_match = re.search(
        r'((https?://)?(www\.)?linkedin\.com[^\s]*)', text, re.I
    )
    links["linkedin"] = linkedin_match.group(0) if linkedin_match else None

    # GitHub
    github_match = re.search(
        r'((https?://)?(www\.)?github\.com[^\s]*)', text, re.I
    )
    links["github"] = github_match.group(0) if github_match else None

    return links


# extract phone
def extract_phone(text):
    patterns=[
        r'\+?\d{1,4}[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{1,9}',
        r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',
        r'\d{3}[-.]?\d{3}[-.]?\d{4}']
    
    for pattern in patterns:
        match =re.search(pattern,text)
        if match:
            return match.group(0).strip()
        return None
    

# extract section
def extract_section(text,section_name):
    lines=text.split("\n")
    section_lines=[]
    inside_section=False

    all_headers=["HEADER","SUMMARY","WORK EXPERIENCE","EXPERIENCES","EDUCATION","ACADEMIC QUALIFICATIONS","QUALIFICATIONS","ACADEMIC BACKGROUND","PROJECTS","TECHNOLOGIES AND TOOLS","SKILLS","SOFT SKILLS"," ACHIEVEMENTS AND CERTIFICATIONS"," PUBLICATION","AWARDS","EXTRACURRICULAR ACTIVITIES"," REFEREES"]

    stop_headers = [h.strip().upper() for h in all_headers if h.strip().upper() != section_name.upper()]

    for line in lines:
        line_upper = line.strip().upper()
        if line_upper == section_name.upper() and not inside_section:
            inside_section = True
            continue

        if inside_section:
            if line_upper in stop_headers:
                break
            if line.strip():
                section_lines.append(line.strip())

    return section_lines

# parse resume
def parse_resume(text: str) -> dict:


     # Work Experience
    experience_sections = ["WORK EXPERIENCE", "EXPERIENCES"]
    experience_content = []
    for section in experience_sections:
        content = extract_section(text, section)
        if content:
            experience_content.extend(content)

    # Education
    education_sections = ["EDUCATION", "ACADEMIC QUALIFICATIONS", "QUALIFICATIONS", "ACADEMIC BACKGROUND"]
    education_content = []
    for section in education_sections:
        content = extract_section(text, section)
        if content:
            education_content = content

    # Combine Technologies & Tools + Skills
    skill_tech_sections = ["TECHNOLOGIES AND TOOLS","SKILLS"]
    skill_tech_content = []
    for section in skill_tech_sections:
        content = extract_section(text, section)
        if content:
            skill_tech_content.extend(content)



    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "links": extract_links(text),
        "experience": experience_content,
        "education": education_content,
        "projects": extract_section(text, "PROJECTS"),
        "skills": skill_tech_content,
        "soft_skills": extract_section(text, "SOFT SKILLS"),
        "achievements": extract_section(text, "ACHIEVEMENTS AND CERTIFICATIONS"),
        "publications": extract_section(text, "PUBLICATIONS"),
        "awards": extract_section(text, "AWARDS"),
        "referees": extract_section(text, "REFEREES"),
        "word_count": len(text.split()),
        "has_contact_info": bool(extract_email(text) and extract_phone(text))
    }






