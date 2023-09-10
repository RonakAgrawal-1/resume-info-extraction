import streamlit as st
import re
from PyPDF2 import PdfReader
from io import BytesIO
import docx2txt  # Add this import for DOC file support
from .skills_keywords import skills_keywords

# Function to extract text from a DOC file
def extract_text_from_docx(uploaded_file):
    try:
        text = docx2txt.process(uploaded_file)
        return text
    except Exception as e:
        return {"error": str(e)}

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    try:
        resume_content = uploaded_file.read()
        pdf = PdfReader(BytesIO(resume_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return {"error": str(e)}

# Function to extract the candidate's name from the resume
def extract_candidate_name(text):
    try:
        name_pattern = r'\b[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*\b'
        candidate_name = re.search(name_pattern, text)
        return candidate_name.group() if candidate_name else "Name not found"
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the resume text
def extract_candidate_skills(text):
    try:
        skills = [skill for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the user-provided job description text
def extract_job_description_skills(job_description_text):
    try:
        skills = [skill for skill in skills_keywords if re.search(rf'\b{skill}\b', job_description_text, re.IGNORECASE)]
        return skills
    except Exception as e:
        return {"error": str(e)}

# Calculate the matching score and common skills based on common skills
def calculate_matching_score_and_common_skills(candidate_skills, job_skills):
    common_skills = list(set(candidate_skills) & set(job_skills))
    total_skills = len(set(candidate_skills + job_skills))
    score = len(common_skills) / total_skills if total_skills > 0 else 0
    return score, common_skills

# Set Streamlit page title and icon
st.set_page_config(
    page_title="Resume Info Extractor",
    page_icon=":page_with_curl:"
)

# Main content
st.title("Resume Information Extractor")

# Add instructions
st.write("Welcome to the Resume Information Extractor!")
st.write("Upload your resume and enter the job description")
st.write("Click the 'Analyze' button to see the results.")
st.markdown("---")

# File upload section for user's resume
st.sidebar.title("Upload Your Resume (PDF or DOC)")
uploaded_file = st.sidebar.file_uploader("Upload a resume file", type=["pdf", "doc", "docx"])

# Text input section for job description
st.sidebar.title("Enter the Job Description (Text)")
job_description_text = st.sidebar.text_area("Enter the job description", "")

# Results section
if uploaded_file and job_description_text:
    st.sidebar.write("You can now analyze:")
    if st.sidebar.button("Analyze"):
        with st.spinner("Analyzing..."):
            # Extract text from the uploaded resume file
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a PDF or DOC/DOCX file.")
                st.stop()

            # Extract skills from the user-provided job description text
            extracted_skills_job_desc = extract_job_description_skills(job_description_text)

            # Extract skills from the resume text
            extracted_skills = extract_candidate_skills(resume_text)

            # Calculate the matching score and common skills
            score, common_skills = calculate_matching_score_and_common_skills(extracted_skills, extracted_skills_job_desc)

            st.success("Analysis complete!")

            # Display results
            st.subheader("Candidate Name:")
            candidate_name = extract_candidate_name(resume_text)
            st.write(f"**Name:** {candidate_name}")

            st.subheader("Matching Score:")
            st.write(f"**Matching Score:** {score:.2%}")

            st.subheader("Common Skills:")
            if common_skills:
                st.write(", ".join(common_skills))
            else:
                st.warning("No common skills found between the job description and the candidate's skills.")
elif uploaded_file:
    st.sidebar.warning("Please enter a job description to proceed.")
elif job_description_text:
    st.sidebar.warning("Please upload your resume to proceed.")
else:
    st.sidebar.warning("Please upload your resume and enter a job description to get started.")
