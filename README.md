# 🤖 AI-Based Resume Screening System

An intelligent resume screening tool that evaluates a candidate's resume 
against a job role and calculates a skill-matching percentage — 
simulating a real-world ATS (Applicant Tracking System).

## 🚀 Features
- Upload PDF resumes
- Select from multiple job roles
- NLP-based skill extraction
- TF-IDF + Cosine Similarity scoring
- Instant eligibility decision

## 🛠️ Tech Stack
- Python, Streamlit, scikit-learn, NLTK, pdfplumber

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 System Workflow
Resume Upload → Text Extraction → NLP Preprocessing → 
Skill Matching → Score Calculation → Eligibility Decision
