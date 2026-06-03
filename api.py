from fastapi import FastAPI, Request
from groq import Groq
import os

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/")
def home():
    return {"status": "AI Malam API is running"}

@app.post("/api")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": message}]
    )
    return {"reply": response.choices[0].message.content}
