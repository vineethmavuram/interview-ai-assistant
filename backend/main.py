from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
import json 

# Load environment variables
load_dotenv()

with open("profile.json", "r") as f:
    candidate_profile = json.load(f)

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
@app.post("/ask")
def ask_question(req: QuestionRequest):

    try:

        prompt = f"""
You are an interview assistant.

Answer as this candidate.

Candidate Profile:

Name:
{candidate_profile['name']}

Role:
{candidate_profile['title']}

Experience:
{candidate_profile['experience_years']} years

Skills:
{', '.join(candidate_profile['skills'])}

Responsibilities:
{', '.join(candidate_profile['current_responsibilities'])}

Projects:
{', '.join(candidate_profile['projects'])}

Question:
{req.question}

Instructions:
- Answer in first person.
- Do not invent experience.
- Keep answer interview-ready.
- Keep answer under 60 seconds.
- Provide keywords.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return {
            "answer": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }