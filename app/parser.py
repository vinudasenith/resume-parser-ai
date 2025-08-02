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
    match =re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else None


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
    

def extract_links(text):
    github=re.search(r'(https?://github\.com/[^\s]+)', text, re.IGNORECASE)
    linkedin=re.search(r'(https?://linkedin\.com/in/[^\s]+)', text, re.IGNORECASE)
    return{
        "github":github.group(0) if github else None,
        "linkedin":linkedin.group(0) if linkedin else None
    }





