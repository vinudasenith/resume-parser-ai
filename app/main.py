from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.parser import parse_resume,extract_text_from_pdf
from app.ranker import (score_resume,get_score_grade,calculate_ats_compatibility,generate_smart_recommendations)

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

    score_data = score_resume(parsed_data, job_description="Software Engineer")  


    if score_data is None:
        return{
            "parsed_data":parsed_data,
            "resume_score":None,
            "score_grade":None,
            "ats_compatibility":0,
            "smart_tips":"Resume scoring failed",
            # "raw_text":text
        }
    
    resume_score=score_data.get("score",0)
    score_grade=get_score_grade(resume_score)
    ats_compatibility=score_data.get("ats_compatibility",0)
    smart_tips=score_data.get("smart_tips",[])


    return {
        "parsed_data": parsed_data,
        "resume_score": resume_score,
        "score_grade": score_grade,
        "ats_compatibility": ats_compatibility,
        "smart_tips": smart_tips,
        # "raw_text": text
    }

