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





