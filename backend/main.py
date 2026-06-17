from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
import json 
from fastapi import UploadFile, File
from docx import Document
from pypdf import PdfReader


# Load environment variables
load_dotenv()

with open("profile.json", "r") as f:
    candidate_profile = json.load(f)

def extract_text_from_docx(file_path):

    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


# Get API key from .env
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in .env file")

# Initialize Groq client
client = Groq(api_key=api_key)

# Create FastAPI app
app = FastAPI()


# Request model
class QuestionRequest(BaseModel):
    question: str


# Health check endpoint
@app.get("/")
def home():
    return {
        "message": "Interview AI Backend Running"
    }


# Interview assistant endpoint
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    try:

        file_path = f"uploads/{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        if file.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(file_path)

        elif file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_path)

        else:
            return {
                "error":
                "Only PDF and DOCX supported"
            }

        return {
            "message":
            "Resume uploaded successfully",
            "characters":
            len(resume_text)
        }

    except Exception as e:

        return {
            "error": str(e)
        }