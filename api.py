from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="AI TEACH API")

# Allow your frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def root():
    return {"status": "AI TEACH API is live 🚀"}

@app.post("/ask")
def ask(msg: Message):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": msg.message}]
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code!= 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    reply = res.json()["choices"][0]["message"]["content"]
    return {"reply": reply}

@app.get("/ask")
def ask_get(message: str = "Hello"):
    return {"reply": f"You said: {message}. Use POST for real AI replies."}
