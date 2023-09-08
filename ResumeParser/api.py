from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Optional
from PyPDF2 import PdfReader
from io import BytesIO
import re
from skills_keywords import skills_keywords

app = FastAPI()

uploaded_file_content = None

# Custom exceptions
class ResumeUploadError(Exception):
    def __init__(self):
        self.status_code = 400
        self.detail = "Please upload a PDF resume first"

class ResumeProcessingError(Exception):
    def __init__(self, message):
        self.status_code = 500
        self.detail = message

# Function to upload the PDF resume
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile):
    global uploaded_file_content
    try:
        uploaded_file_content = await file.read()
        return {"message": "File uploaded successfully!"}
    except Exception as e:
        raise ResumeUploadError()

# Function to extract the candidate's name from the resume
@app.post("/extract_candidate_name/")
async def extract_candidate_name():
    global uploaded_file_content
    try:
        if uploaded_file_content is None:
            raise ResumeUploadError()

        pdf = PdfReader(BytesIO(uploaded_file_content))
        first_page_text = pdf.pages[0].extract_text()
        name_pattern = r'\b[A-Z][a-zA-Z]* [A-Z][a-zA-Z]*\b'
        candidate_name = re.search(name_pattern, first_page_text)
        return {"candidate_name": candidate_name.group()} if candidate_name else {"error": "Name not found"}
    except Exception as e:
        raise ResumeProcessingError("Error while extracting candidate name")

# Function to extract skills from the resume
@app.post("/extract_candidate_skills/")
async def extract_candidate_skills():
    global uploaded_file_content
    try:
        if uploaded_file_content is None:
            raise ResumeUploadError()

        pdf = PdfReader(BytesIO(uploaded_file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        skills = [skill for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]
        return {"skills": skills}
    except Exception as e:
        raise ResumeProcessingError("Error while extracting skills")

# Function to extract certifications, hobbies, and interests from the resume
@app.post("/extract_certifications_hobbies_interests/")
async def extract_certifications_hobbies_interests(max_certifications: Optional[int] = 3):
    global uploaded_file_content
    try:
        if uploaded_file_content is None:
            raise ResumeUploadError()

        pdf = PdfReader(BytesIO(uploaded_file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        # Define a regular expression pattern to extract certifications, hobbies, and interests section
        certifications_pattern = r'(?i)CERTIFICATES[\s\S]*?(?=Skills|$)'
        certifications_match = re.search(certifications_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if certifications_match:
            certifications_text = certifications_match.group(0)
            # Split certifications using newline characters
            certifications_list = [cert.strip() for cert in certifications_text.split('\n') if cert.strip()]
            # Remove the first certification
            certifications_list = certifications_list[1:]
            return {"certifications_hobbies_interests": certifications_list[:max_certifications]}
        else:
            raise ResumeProcessingError("Certifications, hobbies, and interests section not found in the resume.")
    except Exception as e:
        raise ResumeProcessingError("Error while extracting certifications, hobbies, and interests")

# Error handling for custom exceptions
@app.exception_handler(ResumeUploadError)
async def handle_resume_upload_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(ResumeProcessingError)
async def handle_resume_processing_error(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

