import streamlit as st
from skills_data import JOB_ROLES, THRESHOLD
from extractor import extract_text_from_pdf, preprocess_text
from matcher import calculate_match_score, get_matched_skills

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI-Based Resume Screening System")
st.markdown("*Simulate an ATS — check if your resume matches the job role!*")
st.divider()

# ─── Sidebar ───────────────────────────────────────────────────
st.sidebar.header("⚙️ Settings")
threshold = st.sidebar.slider("Eligibility Threshold (%)", 40, 90, THRESHOLD)
st.sidebar.markdown("---")
st.sidebar.markdown("**How it works:**")
st.sidebar.markdown("1. Select a Job Role\n2. Upload your Resume (PDF)\n3. Get your Match Score!")

# ─── Job Role Selection ────────────────────────────────────────
st.subheader("📌 Step 1: Select Job Role")
selected_role = st.selectbox("Choose the job role you're applying for:", list(JOB_ROLES.keys()))

required_skills = JOB_ROLES[selected_role]
st.markdown(f"**Required Skills for {selected_role}:**")
st.info("  •  " + "   •  ".join([s.title() for s in required_skills]))

# ─── Resume Upload ─────────────────────────────────────────────
st.subheader("📄 Step 2: Upload Your Resume")
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

# ─── Analysis ─────────────────────────────────────────────────
if uploaded_file is not None:
    st.subheader("🔍 Step 3: Analysis Results")
    
    with st.spinner("Extracting and analyzing your resume..."):
        # Extract text
        raw_text = extract_text_from_pdf(uploaded_file)
        
        if not raw_text.strip():
            st.error("Could not extract text from PDF. Please try a text-based PDF.")
        else:
            # Preprocess
            clean_text = preprocess_text(raw_text)
            
            # Calculate score
            score = calculate_match_score(clean_text, required_skills)
            matched, missing = get_matched_skills(raw_text, required_skills)
            
            # ── Display Score ──────────────────────────
            st.markdown("### 📊 Match Score")
            col1, col2, col3 = st.columns(3)
            col1.metric("Match Score", f"{score}%")
            col2.metric("Skills Matched", f"{len(matched)}/{len(required_skills)}")
            col3.metric("Threshold", f"{threshold}%")
            
            # Progress bar
            st.progress(min(int(score), 100))
            
            # ── Eligibility Decision ───────────────────
            st.markdown("### 🏆 Eligibility Decision")
            if score >= threshold:
                st.success(f"✅ Congratulations! You ARE ELIGIBLE for the **{selected_role}** role.")
                st.balloons()
            else:
                st.error(f"❌ Sorry, you are NOT ELIGIBLE for the **{selected_role}** role.")
                st.markdown(f"*Your score ({score}%) is below the required threshold ({threshold}%).*")
            
            # ── Skill Breakdown ────────────────────────
            st.markdown("### 🧩 Skill Breakdown")
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("**✅ Matched Skills:**")
                if matched:
                    for skill in matched:
                        st.markdown(f"- ✅ {skill.title()}")
                else:
                    st.markdown("*No exact skill matches found.*")
            
            with col_b:
                st.markdown("**❌ Missing Skills:**")
                if missing:
                    for skill in missing:
                        st.markdown(f"- ❌ {skill.title()}")
                else:
                    st.markdown("*You have all required skills!*")
            
            # ── Resume Preview ─────────────────────────
            with st.expander("📋 View Extracted Resume Text"):
                st.text(raw_text[:2000] + ("..." if len(raw_text) > 2000 else ""))


