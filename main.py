import site
site.addsitedir(r"C:\Users\TANISHA V SHETTY\AppData\Roaming\Python\Python38\site-packages")

from Job_Description_Summarizer.jd_summarizer import summarize_job_description
from CV_Reader.cv_reader import parse_cv
from Matching_and_shortlisting.matching_algorithm import calculate_match_score
from Interview_scheduler.interview_scheduler import send_interview_invite
from Database.sqlite_database import initialize_db, insert_candidate
from config import MATCH_THRESHOLD, DEFAULT_CANDIDATE_NAME, DEFAULT_CANDIDATE_EMAIL

# Load input

import os
import fitz  # For PDFs
from docx import Document  # For Word docs

# Define folder path
folder_path = r"C:\Users\TANISHA V SHETTY\OneDrive\Desktop\JobScreeningAI\Dataset\[Usecase 5] AI-Powered Job Application Screening System\CVs1"
jd_text = """
We are hiring a Machine Learning Engineer with experience in Python, TensorFlow or PyTorch, and data preprocessing.
Must have good knowledge of model evaluation and deployment on cloud platforms like AWS or GCP.
"""

jd_summary = summarize_job_description(jd_text)

# Dictionary to store file content
cv_data = {}

# Loop through all files
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    text = ""

    try:
        if filename.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()

        elif filename.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            print(f"Skipping unsupported file: {filename}")
            continue

        # Store content
        cv_data[filename] = text

    except Exception as e:
        print(f"Error reading {filename}: {e}")

# ✅ Print summary
for name, content in cv_data.items():
    print(f"\n--- {name} ---")
    print(content[:500], "...\n")  # Show a preview


# Step 1: Init DB
initialize_db()

# Step 2: Run agents
jd_summary = summarize_job_description(jd_text)
cv_summary = parse_cv(cv_text)

# Step 3: Match score
score = calculate_match_score(jd_summary, cv_summary)
print(f"\n✅ Match Score: {score}%")

# Step 4: Shortlist and schedule
if score >= MATCH_THRESHOLD:
    insert_candidate(DEFAULT_CANDIDATE_NAME, DEFAULT_CANDIDATE_EMAIL, cv_summary, score)
    send_interview_invite(DEFAULT_CANDIDATE_NAME, DEFAULT_CANDIDATE_EMAIL, score)
else:
    print("\n❌ Candidate did not meet the threshold.")
