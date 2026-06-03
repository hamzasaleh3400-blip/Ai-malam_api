from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI(title="AI TEACH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "AI TEACH API is live 🚀"}

@app.post("/ask")
def ask(msg: Message):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": msg.message}]
    )
    return {"reply": completion.choices[0].message.content}
