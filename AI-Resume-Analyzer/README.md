# AI-Powered Resume Analyzer

This repository contains a starter project for an AI-powered resume analyzer.
It includes:
- FastAPI backend: `backend/main.py` (resume parsing, skill extraction, scoring)
- Simple frontend: `frontend/index.html` (upload UI + results)

## How to run

### Backend
```bash
cd backend
python -m venv .venv
# On Windows CMD:
.venv\Scripts\activate
# On PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
python -m http.server 5500
# Visit http://127.0.0.1:5500
```

## Notes
- The backend attempts to use `sentence-transformers` if installed for semantic similarity. If not available it falls back to TF-IDF.
- spaCy usage requires `python -m spacy download en_core_web_sm` if you want NER-based skill extraction.
- This is a starter scaffold — extend with better parsers, a skills ontology, and improved scoring for production use.
