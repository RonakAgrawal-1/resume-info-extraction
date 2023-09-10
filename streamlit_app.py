import streamlit as st
import re
from PyPDF2 import PdfReader
from io import BytesIO
import docx2txt

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
        skills = list(set([skill.lower() for skill in skills_keywords if re.search(rf'\b{skill}\b', text, re.IGNORECASE)]))
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to extract skills from the user-provided job description text
def extract_job_description_skills(job_description_text):
    try:
        skills = list(set([skill.lower() for skill in skills_keywords if re.search(rf'\b{skill}\b', job_description_text, re.IGNORECASE)]))
        return skills
    except Exception as e:
        return {"error": str(e)}

# Function to calculate the matching score based on skills
def calculate_matching_score(candidate_skills, job_description_text):
    job_skills = extract_job_description_skills(job_description_text)
    common_skills = list(set(candidate_skills) & set(job_skills))
    
    if job_skills:
        score = len(common_skills) / len(job_skills)
    else:
        score = 0.0
    
    return score, common_skills

# Set Streamlit page title and icon
st.set_page_config(
    page_title="Resume Info Extractor",
    page_icon=":page_with_curl:"
)

# Introduction Section
st.title("Welcome to the Resume Information Extractor!")
st.write("This tool helps you extract and analyze information from resumes.")
st.write("Follow these steps to get started:")
st.markdown("1. Upload a resume in PDF or DOC/DOCX format.")
st.markdown("2. Enter the job description.")
st.markdown("3. Click the 'Analyze' button to see the results.")

# Create a sidebar for inputs
st.sidebar.title("Resume Info Extractor")

# Upload Resume Section
st.sidebar.subheader("Step 1: Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF or DOC/DOCX)")

# Enter Job Description Section
st.sidebar.subheader("Step 2: Enter Job Description")
job_description_text = st.sidebar.text_area("Enter the job description")

# Analyze Button in Sidebar
if st.sidebar.button("Analyze"):
    if not uploaded_file or not job_description_text:
        st.warning("Please complete both steps to analyze.")
    else:
        with st.spinner("Analyzing..."):
            # Extract text from the uploaded resume file
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a PDF or DOC/DOCX file.")
                st.stop()

            # Extract skills from the candidate's resume text
            extracted_skills = extract_candidate_skills(resume_text)
            
            # Calculate the matching score
            score, common_skills = calculate_matching_score(extracted_skills, job_description_text)

            # Display Results Section
            st.title("Analysis Results")

            # Candidate Name
            st.subheader("Candidate Name")
            candidate_name = extract_candidate_name(resume_text)
            st.write(f"The candidate's name is: {candidate_name}")

            # Matching Score
            st.subheader("Matching Score")
            st.write(f"The matching score with the job description is: {score:.2%}")

            # Skills Extracted
            st.subheader("Skills Extracted from Resume")
            if extracted_skills:
                st.write(", ".join(extracted_skills))
            else:
                st.warning("No skills found in the resume.")

            # Common Skills
            st.subheader("Common Skills with Job Description")
            if common_skills:
                st.write(", ".join(common_skills))
            else:
                st.warning("No common skills found between the job description and the candidate's skills.")

# List of skills and keywords
skills_keywords = [
    "python", "java", "javascript", "c++", "c#", ".net", "ruby", "php",
    "html", "css", "javascript", "frontend development", "backend development",
    "full-stack development", "responsive design", "web services", "REST API",
    "sql", "database management", "data modeling", "data analysis", "big data",
    "data warehousing", "ETL", "NoSQL",
    "data structures", "algorithms", "algorithm design",
    "software development", "object-oriented programming", "functional programming",
    "frameworks", "software architecture", "design patterns", "code review",
    "code optimization", "software documentation",
    "devops", "docker", "kubernetes", "continuous integration", "CI/CD", "git", "Jenkins",
    "Ansible", "Terraform", "Infrastructure as Code (IaC)", "Continuous Delivery",
    "cloud computing", "AWS", "Azure", "Google Cloud", "Heroku", "AWS Lambda",
    "serverless", "cloud-native", "cloud security", "cloud architecture", "microservices",
    "testing", "automation", "software testing", "Junit", "Selenium", "test strategy",
    "TDD", "BDD", "functional testing", "load testing",
    "machine learning", "deep learning", "artificial intelligence",
    "natural language processing", "data mining", "computer vision",
    "algorithm design", "AI", "ML", "Kafka", "TensorFlow",
    "security", "penetration testing", "OWASP",
    "version control", "Git", "SVN",
    "agile methodology", "scrum", "Kanban",
    "leadership", "team building", "technology leadership", "interpersonal skills",
    "problem solving", "critical thinking", "debugging", "root cause analysis",
    "communication", "presentation", "technical writing", "Swagger", "API documentation",
    "collaboration", "teamwork", "cross-functional teams",
    "Linux/Unix", "bash scripting", "system administration", "AWS CLI",
    "networking", "stress management", "decision-making",
    "conflict resolution", "negotiation", "time management", "SCRUM Master",
    "software manager", "technology manager", "DevOps engineer", "Data Engineer",
    "IoT", "blockchain", "chatbots", "Microservice", "Distributed Systems",
    "software testing", "test automation", "unit testing", "integration testing",
    "real-time systems", "low-level programming", "RTOS", "embedded systems", "GPU programming",
    "concurrency", "distributed computing", "scalability", "performance tuning", "memory management",
    "network protocols", "backend architecture", "API design", "microservices architecture",
    "cloud-native", "serverless", "performance monitoring", "continuous delivery", "refactoring",
    "code quality", "code profiling", "dependency management", "software development lifecycle",
    "software design", "architecture patterns", "application security", "encryption",
    "authentication", "authorization", "web security", "vulnerability assessment",
    "secure coding practices", "SAST", "DAST", "agile project management", "sprint planning",
    "agile ceremonies", "sprint review", "sprint retrospective", "pair programming",
    "code collaboration tools", "code versioning tools", "continuous integration/continuous deployment",
    "software development methodologies", "technical debt management", "code reviews",
    "system design", "technical leadership", "coding standards", "software engineering best practices",
    "distributed version control", "architectural design principles", "software estimation",
    "software prototyping", "change management", "business process optimization",
    "root cause analysis", "problem management", "incident response", "release management",
    "Kubernetes", "Docker Swarm", "Continuous Deployment", "Site Reliability Engineering (SRE)",
    "Infrastructure Automation", "Container Orchestration", "Configuration Management",
    "Monitoring and Alerting", "Log Management", "Serverless Computing", "CICD Pipelines",
    "Load Balancing", "GitOps", "Cloud Cost Optimization",
    "AWS", "Azure", "Google Cloud", "Heroku", "Cloud Security", "Serverless Computing",
    "Cloud Architecture", "Microservices", "DevOps in the Cloud",
    "Neural Networks", "Deep Learning Frameworks", "Computer Vision Libraries", "NLP Libraries",
    "AI Model Training", "Model Deployment", "Machine Learning Pipelines", "AI/ML Ethics",
    "Team Building", "Team Leadership", "Team Collaboration", "Conflict Resolution",
    "Team Motivation", "Team Productivity", "Empowering Teams",
    "PostgreSQL",  # Add PostgreSQL
    "database administration",  # Add related keyword
    "SQL queries",  # Add related keyword
    "spring",  # Add Spring
    "spring boot",  # Add Spring Boot
    "MVC",  # Add MVC
]

# Run the Streamlit app
if __name__ == "__main__":
    main()
