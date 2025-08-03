import io
import re
import pdfplumber
import spacy

#load spacy NLP model
nlp=spacy.load("en_core_web_sm")


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


def extract_email(text):
    #email pattern
    match =re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else None


def extract_phone(text):
    #better phone pattern for various formats
    patterns=[
        r'\+?\d{1,4}[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{1,9}',
        r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',
        r'\d{3}[-.]?\d{3}[-.]?\d{4}']
    
    for pattern in patterns:
        match =re.search(pattern,text)
        if match:
            return match.group(0).strip()
        return None
    

def extract_links(text):
    github=re.search(r'(https?://github\.com/[^\s]+)', text, re.IGNORECASE)
    linkedin=re.search(r'(https?://linkedin\.com/in/[^\s]+)', text, re.IGNORECASE)
    return{
        "github":github.group(0) if github else None,
        "linkedin":linkedin.group(0) if linkedin else None
    }

def extract_section(text,section_name):
    lines=text.split("\n")
    section_lines=[]
    inside_section=False

    #section header to stop 
    stop_sections=["EDUCATIONS","PROJECTS","EXPERIENCES","SKILLS","REFERENCES","PROFILE","EXTRA-CURRICULAR","TEAMWORK"]

    #start capturing lines after section header
    for line in lines:
        line_upper=line.strip().upper()

        if section_name.upper() in line_upper:
            inside_section=True
            continue

        #stop capturing when we hit another section
        if inside_section:
            if any(stop in line_upper for stop in stop_sections) and line_upper!=section_name.upper():
                break
            if line.strip():
                section_lines.append(line.strip())

    return section_lines

def extract_skills(text):

    skill_keywords=[
        "Java", "Python", "JavaScript", "C", "C++", "C#", "PHP", "Go", "Rust","HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "MongoDB", "MySQL", "PostgreSQL", "SQL", "DBMS", "Redis","Git", "Docker", "AWS", "Azure", "Firebase", "REST API", "GraphQL","Machine Learning", "Data Analysis", "Agile", "Scrum"
    ]

    found_skills=[]
    text_lower=text.lower()

    for skill in skill_keywords:
        #check for each
        skill_variants=[skill.lower(),skill.lower().replace('.',''),skill.lower().replace(' ','')]
        if any(variant in text_lower for variant in skill_variants):
            found_skills.append(skill)

    return list(set(found_skills))

def parse_resume(text:str) ->dict:
    if not text.strip():
        return {"error":"No text content found"}
    
    doc = nlp(text)

    #Extract name(first PERSON entity found)
    for ent in doc.ents:
        if ent.label_=="PERSON" and len(ent.text.split())<=3:
            name=ent.text
            break

    projects_text="\n".join(extract_section(text,"PROJECTS"))
    project_links=extract_links_from_text(projects_text)

    return {
        "name": name,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "links": extract_links(text),
        "education": extract_section(text, "EDUCATION"),
        "experience": extract_section(text, "EXPERIENCE"),  # Added experience section
        "projects": extract_section(text, "PROJECTS"),
        "project_links": project_links,
        "skills": extract_skills(text),
        "extra_curricular_activities": extract_section(text, "EXTRA-CURRICULAR ACTIVITIES"),
        "teamwork_experience": extract_section(text, "TEAMWORK EXPERIENCE"),
        "referees": extract_section(text, "REFEREES"),
        "profile_summary": extract_section(text, "PROFILE"),
        "word_count": len(text.split()),
        "has_contact_info": bool(extract_email(text) and extract_phone(text))
    }

def extract_links_from_text(text):
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return urls






