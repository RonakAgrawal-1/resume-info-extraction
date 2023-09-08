```markdown
# Resume Information Extraction

This project consists of two Python applications: "app.py" and "api.py," which allow you to extract information from PDF resumes, such as the candidate's name, skills, and certifications. Below are instructions on how to run both applications.

## Prerequisites

Before running the applications, make sure you have the following prerequisites installed on your system:

- Python 3.x ([Download Python](https://www.python.org/downloads/))
- pip (Python package manager)

## Setup

### Clone the Repository

Clone this Git repository to your local machine using the following command:

```bash
git clone https://github.com/RonakAgrawal-1/resume-info-extraction.git
```

### Navigate to the Project Directory

Change your current working directory to the project directory:

```bash
cd resume-info-extraction
```

### Install Dependencies

You need to install the required Python packages specified in the "requirements.txt" file.

```bash
pip install -r requirements.txt
```

## Running the Applications

### "app.py" - Streamlit Web Application

To run the "app.py" Streamlit web application, follow these steps:

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. The application will launch in your default web browser. You can upload PDF resumes and extract information as needed.

### "api.py" - FastAPI API

To run the "api.py" FastAPI API, follow these steps:

1. Run the FastAPI application using Uvicorn:

   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000
   ```

2. The API will start and be accessible at `http://localhost:8000`. You can use API client tools like `curl` or explore the API using a web browser or API testing tools like Postman.

## Usage

### "app.py" - Streamlit Web Application

- Open the Streamlit application in your web browser.
- Upload a PDF resume.
- Extract candidate information such as name, skills, and certifications using the provided buttons.

### "api.py" - FastAPI API

- The API endpoints are accessible at `http://localhost:8000`.
- You can use HTTP POST requests to upload PDF resumes and retrieve information from the following endpoints:
  - `/upload_resume/`: Upload a PDF resume.
  - `/extract_candidate_name/`: Extract the candidate's name from the uploaded resume.
  - `/extract_candidate_skills/`: Extract skills from the uploaded resume.
  - `/extract_certifications_hobbies_interests/`: Extract certifications, hobbies, and interests from the uploaded resume.

## Contributors

- [Ronak Agrawal](https://github.com/RonakAgrawal-1)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
```