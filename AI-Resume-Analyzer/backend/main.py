from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import PyPDF2
import docx
import spacy
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load NLP models
nlp = spacy.load("en_core_web_sm")
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Predefined skills dictionary
SKILLS_DB = [
    "Python","Java","C++","JavaScript","TypeScript","C#","Go","R","Ruby","PHP",
    "HTML","CSS","React","Angular","Vue","Node.js","Django","Flask","Spring Boot",
    "SQL","MySQL","PostgreSQL","MongoDB","Oracle","SQLite",
    "AWS","Azure","Google Cloud","Docker","Kubernetes","Terraform",
    "Pandas","NumPy","Matplotlib","Scikit-learn","TensorFlow","PyTorch",
    "Machine Learning","Deep Learning","NLP","Computer Vision",
    "Git","GitHub","CI/CD","Jenkins","Linux",
    "Leadership","Teamwork","Communication","Problem Solving","Critical Thinking"
]

# Extract text from resume
def extract_text(file_path: str) -> str:
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return text

# Extract skills from predefined dictionary
def extract_skills(text: str):
    found = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(set(found))

@app.post("/analyze_resume/")
async def analyze_resume(resume: UploadFile = File(...), job_description: str = Form(...)):
    file_path = f"temp_{resume.filename}"
    with open(file_path, "wb") as f:
        f.write(await resume.read())

    resume_text = extract_text(file_path)
    os.remove(file_path)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # Semantic similarity
    resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = sbert_model.encode(job_description, convert_to_tensor=True)
    similarity_score = util.cos_sim(resume_embedding, jd_embedding).item()

    suggestions = [s for s in jd_skills if s not in resume_skills]

    return {
        "filename": resume.filename,
        "skills": resume_skills,
        "match_score": round(similarity_score,2),
        "suggestions": suggestions
    }
