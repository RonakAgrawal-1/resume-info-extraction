import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
import re
from skills_keywords import skills_keywords

# Function to extract the candidate's name from the resume
def extract_candidate_name(uploaded_file):
    try:
        resume_content = uploaded_file.read()
        pdf = PdfReader(BytesIO(resume_content))
        first_page_text = pdf.pages[0].extract_text()
        name_pattern = r'\b[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*\b'
        candidate_name = re.search(name_pattern, first_page_text)
        return candidate_name.group() if candidate_name else "Name not found"
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the resume
def extract_candidate_skills(uploaded_file):
    try:
        resume_content = uploaded_file.read()
        text = ""
        pdf = PdfReader(BytesIO(resume_content))
        for page in pdf.pages:
            text += page.extract_text()
        skills = [skill for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to extract certifications from the resume
def extract_certifications(uploaded_file, max_certifications=3):
    try:
        resume_content = uploaded_file.read()
        text = ""
        pdf = PdfReader(BytesIO(resume_content))
        for page in pdf.pages:
            text += page.extract_text()
        
        # Define a regular expression pattern to extract certifications section
        certifications_pattern = r'(?i)CERTIFICATES[\s\S]*?(?=Skills|$)'
        certifications_match = re.search(certifications_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if certifications_match:
            certifications_text = certifications_match.group(0)
            # Split certifications using newline characters
            certifications_list = [cert.strip() for cert in certifications_text.split('\n') if cert.strip()]
            # Remove the first certification
            certifications_list = certifications_list[1:]
            return certifications_list[:max_certifications]
        else:
            return "Certifications section not found in the resume."
    except Exception as e:
        return {"error": str(e)}

# Set Streamlit page title and icon
st.set_page_config(
    page_title="Resume Info Extractor",
    page_icon=":page_with_curl:"
)

# Create a Streamlit sidebar
st.sidebar.title("Resume Info Extractor")

# Main content
st.title("Resume Information Extractor")

# File upload section
uploaded_file = st.file_uploader("Upload a PDF resume", type=["pdf"])

if uploaded_file:
    st.info("File uploaded successfully!")

    if st.button("Extract Candidate Name"):
        candidate_name = extract_candidate_name(uploaded_file)
        if candidate_name == "Name not found":
            st.warning("Candidate name not found in the resume.")
        else:
            st.success(f"**Candidate Name:** {candidate_name}")

    if st.button("Extract Skills"):
        extracted_skills = extract_candidate_skills(uploaded_file)
        if "error" in extracted_skills:
            st.error("Error: " + extracted_skills["error"])
        else:
            st.header("Skills extracted from the resume:")
            if extracted_skills:
                skill_data = [{"Skills": skill} for skill in extracted_skills]
                st.table(skill_data)
            else:
                st.warning("No skills found in the resume.")

    if st.button("Extract Certifications"):
        certifications_info = extract_certifications(uploaded_file, max_certifications=3)
        if certifications_info == "Certifications section not found in the resume.":
            st.warning(certifications_info)
        else:
            st.header("Certifications extracted from the resume:")
            if certifications_info:
                for idx, certification in enumerate(certifications_info, start=1):
                    st.write(f"{idx}. {certification}")
            else:
                st.warning("No certifications found in the resume.")
                