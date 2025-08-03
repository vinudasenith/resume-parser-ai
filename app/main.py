from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.parser import parse_resume,extract_text_from_pdf
from app.ranker import score_resume

app=FastAPI(title="Resume Parser Microservice (No LLM)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "No text found in PDF"}

    parsed_data = parse_resume(text)

    score = score_resume(parsed_data, job_description="Software Engineer")  

    return {
        "parsed_data": parsed_data,
        "resume_score": score,
        "raw_text": text
    }

