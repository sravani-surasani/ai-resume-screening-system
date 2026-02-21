from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, required_skills):
    """
    Calculate match score based on direct skill presence (primary)
    + TF-IDF cosine similarity (secondary boost).
    Returns match percentage (0-100).
    """
    resume_lower = resume_text.lower()

    # Primary: Count how many required skills are present in resume
    matched_skills = [skill for skill in required_skills if skill.lower() in resume_lower]
    skill_match_ratio = len(matched_skills) / len(required_skills)  # 0.0 to 1.0

    # Secondary: TF-IDF cosine similarity as a small boost
    try:
        skills_text = " ".join(required_skills)
        corpus = [resume_lower, skills_text.lower()]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        tfidf_score = 0.0

    # Final score: 80% weight on skill matching + 20% weight on TF-IDF
    final_score = (skill_match_ratio * 0.80 + tfidf_score * 0.20) * 100
    final_score = round(min(final_score, 100), 2)

    return final_score

def get_matched_skills(resume_text, required_skills):
    """Find which required skills are present in the resume."""
    resume_lower = resume_text.lower()
    matched = [skill for skill in required_skills if skill.lower() in resume_lower]
    missing = [skill for skill in required_skills if skill.lower() not in resume_lower]
    return matched, missing