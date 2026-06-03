from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI(title="AI TEACH API")

# Allow your frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from Render Environment Variables
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Question(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "AI TEACH API is live 🚀"}

@app.post("/ask")
def ask_ai(q: Question):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": q.message}]
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
