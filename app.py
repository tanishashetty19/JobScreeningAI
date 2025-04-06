import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from Job_Description_Summarizer.jd_summarizer import summarize_job_description
from CV_Reader.cv_reader import parse_cv
from Matching_and_shortlisting.matching_algorithm import calculate_match_score
from Interview_scheduler.interview_scheduler import send_interview_invite
from Database.sqlite_database import insert_candidate
from config import MATCH_THRESHOLD

# Page config (must be first)
st.set_page_config(page_title="Job Screening AI", layout="centered")

# UI Elements
st.title("🤖 AI-Powered Job Screening")
st.markdown("Upload a JD and CV to calculate candidate match score and send interview invite automatically.")

# Uploaders
jd_file = st.file_uploader("📄 Upload Job Description (.txt or .pdf)", type=["txt", "pdf"])
cv_file = st.file_uploader("👤 Upload Candidate CV (.txt or .pdf)", type=["txt", "pdf"])

# Input fields
candidate_name = st.text_input("Candidate Name", value="John Doe")
candidate_email = st.text_input("Candidate Email", value="john@example.com")

# Run screening
if st.button("🚀 Run Screening", key="run_screening_button"):
    if jd_file is not None and cv_file is not None:
        # Read JD file
        if jd_file.name.lower().endswith(".pdf"):
            jd_text = extract_text_from_pdf(jd_file)
        else:
            jd_text = jd_file.read().decode("utf-8")

        # Read CV file
        if cv_file.name.lower().endswith(".pdf"):
            cv_text = extract_text_from_pdf(cv_file)
        else:
            cv_text = cv_file.read().decode("utf-8")

        # Run the pipeline
        summarized_jd = summarize_job_description(jd_text)
        parsed_cv = parse_cv(cv_text)
        match_score = calculate_match_score(summarized_jd, parsed_cv)

        st.subheader("📝 Match Results")
        st.write(f"**Match Score:** {match_score}%")

        if match_score >= MATCH_THRESHOLD:
            insert_candidate(candidate_name, candidate_email, match_score)
            invite = send_interview_invite(candidate_name, candidate_email)
            st.success("✅ Candidate shortlisted and interview invite sent!")
            st.markdown(f"📧 **Email Preview:**\n\n{invite}")
        else:
            st.warning("❌ Candidate not shortlisted. Match score below threshold.")
    else:
        st.warning("⚠️ Please upload both Job Description and CV files.")
