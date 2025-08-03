import re
from typing import Dict,List

def score_resume(resume_data:dict,job_description:str)->dict:

    #resume scoring with enhanced logic
    if not resume_data or resume_data.get("error"):
        return {"error":"Cannot score resume with parsing","score":0}
    

    #adjust weights under cases
    weights={
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


    skills_score,matched_skills=calculate_skills_score(resume_skills,jd_text)
    experience_score=calculate_experience_score(resume_exp,jd_text)
    education_score=calculate_education_score(resume_edu,jd_text)
    project_score=calculate_project_score(resume_projects,jd_text)
    contact_score=calculate_contact_score(resume_data)

    total_score = (
        skills_score * weights["skills"] +
        experience_score * weights["experience"] +
        education_score * weights["education"] +
        project_score * weights["projects"] +
        contact_score * weights["contact_completeness"]
    ) 


    bonus_score=calculate_bonus_score(resume_data)
    final_score=min(total_score+bonus_score,100)


#calculating skill score with enhanced logic    
def calculate_skills_score(resume_skills:List[str],jd_text:str)->tuple:

    if not resume_skills:
        return 0,[]
    

    #synonyms for skills better matching
    skills_synonyms={
        "javascript": ["js", "node.js", "nodejs", "react", "vue", "angular"],
        "python": ["django", "flask", "fastapi", "pandas", "numpy"],
        "java": ["spring", "hibernate", "maven", "gradle"],
        "database": ["sql", "mysql", "postgresql", "mongodb", "nosql"],
        "web": ["html", "css", "frontend", "backend", "fullstack"],
        "cloud": ["aws", "azure", "gcp", "docker", "kubernetes"]
    }

    matched_skills=[]
    skill_matches=0

    #direct skill match
    for skill in resume_skills:
        if skill in jd_text:
            matched_skills.append(skill)
            skill_matches+=1
        else:
            #synonym match
            for category,synonyms in skills_synonyms.items():
                if skill in synonyms and category in jd_text:
                    matched_skills.append(skill)
                    skill_matches += 0.8  
                    break

    #calculate skill score
    skills_score = min(skill_matches / len(resume_skills), 1.0)
    


    if len(set(matched_skills)) >= 5:
        skills_score = min(skills_score * 1.1, 1.0)
    
    return skills_score, matched_skills


def calculate_experience_score(resume_exp:str,jd_text:str)->float:

    if not resume_exp:
        return 0.0
    
    experience_indicators={
        #experience in years
        "years":0.3,
        "year":0.25,

        #experience in job roles
        "senior": 0.4,
        "lead": 0.4,
        "principal": 0.5,
        "junior": 0.2,
        "intern": 0.15,
        

        "engineer": 0.3,
        "developer": 0.3,
        "programmer": 0.25,
        "analyst": 0.2,
        "consultant": 0.25,
    }

    score=0
    max_possible=sum(experience_indicators.values())

    for indicator, weight in experience_indicators.items():
        if indicator in resume_exp:
            score += weight

            if indicator in jd_text:
                score += weight * 0.5
    
    return min(score / max_possible, 1.0)


def calculate_education_score(resume_edu:str,jd_text:str)->float:

    if not resume_edu:
        return 0.0
    

    education_indicators={

        #levels
        "phd": 0.5, "ph.d": 0.5, "doctorate": 0.5,
        "master": 0.4, "msc": 0.4, "m.sc": 0.4, "mba": 0.35,
        "bachelor": 0.3, "bsc": 0.3, "b.sc": 0.3, "degree": 0.25,
        "diploma": 0.2, "certificate": 0.15,

        "computer": 0.3, "software": 0.3, "information": 0.25,
        "engineering": 0.3, "technology": 0.25, "science": 0.2,
        "mathematics": 0.2, "data": 0.25

    }

    score=0
    max_possible=1.0 

    #add more marks for relevant experience
    for indicator,weight in education_indicators.items():
        if indicator in resume_edu:
            score+=weight

            if indicator in jd_text:
                score+=weight*0.3

    return min(score,max_possible)

def calculate_project_score(resume_projects:str,resume_skills:List[str],jd_text:str)->float:

    if not resume_projects:
        return 0.0
    
    project_score=0

    #checking if project mention relevant skills
    skill_mentions=sum(1 for skill in resume_skills if skill in resume_projects)
    if resume_skills:
        project_score+=(skill_mentions/len(resume_skills))*0.6

    complexity_indicators = ["api", "database", "full-stack", "deployment", "testing", "architecture"]
    complexity_score = sum(1 for indicator in complexity_indicators if indicator in resume_projects)
    project_score += min(complexity_score / len(complexity_indicators), 0.4)
    
    return min(project_score, 1.0)


def calculate_bonus_points(resume_data:dict)->float:

    bonus=0

    # bonus for having git
    if resume_data.get("links",{}).get("github"):
        bonus+=2

    #bonus for having project links
    if resume_data.get("project_links"):
        bonus+=2


    #bonus for having comprehensive sections
    sections=["education","projects","skills","experience"]
    filled_sections=sum(1 for section in sections if resume_data.get(section))
    if filled_sections>=3:
        bonus+=1

    #bonus for having good length
    word_count=resume_data.get("word_count",0)
    if 200<=word_count<=800:
        bonus+=1

    return bonus









