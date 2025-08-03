import re
from typing import Dict,List

def score_resume(resume_data:dict,job_description:str)->dict:

    #resume scoring with enhanced logic
    if not resume_data or resume_data.get("error"):
        return {"error":"Cannot score resume with parsing","score":0}
    

    #adjust weights under cases
    weight={
        "skills":0.35,
        "experience":0.25,
        "education":0.20,
        "projects":0.15,
        "contact_completeness":0.10
    }

    jd_text = job_description.lower()


    resume_skills=[skill.lower() for skill in resume_data.get("skills",[])]
    resume_exp=" ".join(resume_data.get("experience",[])).lower()
    resume_edu=" ".join(resume_data.get("education",[])).lower()
    resume_projects=" ".join(resume_data.get("projects",[])).lower()

    

