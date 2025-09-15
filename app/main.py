from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .resume_parser import parse_resume, extract_text_from_pdf
from .ranker import calculate_ats_compatibility
from .resume_classifier import is_resume_ai_combined  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):

    # Only accept PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read PDF content
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    if not text.strip():
        return {"error": "No text found in PDF"}

    # Check if the document looks like a resume using AI + keywords
    resume_check = is_resume_ai_combined(text)
    if not resume_check:
        return {
            "is_resume": False,
            "message": "The provided document does not look like a resume."
        }

    # Parse resume
    parsed_data = parse_resume(text)

    # Calculate ATS compatibility
    ats_score = calculate_ats_compatibility(parsed_data,text)


    
    print("Email:", parsed_data["email"])
    print("Phone:", parsed_data["phone"])
    print("Links:", parsed_data["links"])
    print("Experience:", parsed_data["experience"])
    print("Education:", parsed_data["education"])
    print("Projects:", parsed_data["projects"])
    print("Skills:", parsed_data["skills"])
    print("Soft Skills:", parsed_data["soft_skills"])
    print("Achievements:", parsed_data["achievements"])
    print("Publications:", parsed_data["publications"])
    print("Awards:", parsed_data["awards"])
    print("Referees:", parsed_data["referees"])
    print("Word Count:", parsed_data["word_count"])
    print("Has Contact Info:", parsed_data["has_contact_info"])

    # Return response
    return {
        "is_resume": True,
        "message": "This looks like a valid resume.",
        "parsed_data": parsed_data,
        "ats_compatibility": ats_score["ats_percentage"],
        "feedback": ats_score["messages"]
    }
