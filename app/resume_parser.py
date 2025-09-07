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
    # email pattern
    match =re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if match:
        return match.group(0).strip()
    return None


# extract phone
def extract_phone(text):
    # better phone pattern for various formats
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

    # section header to stop 
    stop_sections=["EXPERIENCES","EDUCATIONS","PROJECTS","EXPERIENCE","EDUCATION","PROJECT"]


    for line in lines:
        line_upper=line.strip().upper()

        if section_name.upper() in line_upper:
            inside_section=True
            continue


        if inside_section:
            if any(stop in line_upper for stop in stop_sections) and line_upper!=section_name.upper():
                break
            if line.strip():
                section_lines.append(line.strip())

    return section_lines

# parse resume
def parse_resume(text: str) -> dict:

    education_sections = ["EDUCATION", "ACADEMIC QUALIFICATIONS", "QUALIFICATIONS", "ACADEMIC BACKGROUND"]
    education_content = []
    for section in education_sections:
        content = extract_section(text, section)
        if content:
            education_content = content
            break  


    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": education_content,
        "experience": extract_section(text, "EXPERIENCE"),
        "projects": extract_section(text, "PROJECTS"),
        "word_count": len(text.split()),
        "has_contact_info": bool(extract_email(text) and extract_phone(text))
    }






