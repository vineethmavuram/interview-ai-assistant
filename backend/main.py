from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

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

The user is preparing for an interview.

Question:
{req.question}

Provide:

1. Professional Answer
2. Keywords
3. Interview Tips

Keep the answer concise and easy to speak.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return {
            "answer": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }