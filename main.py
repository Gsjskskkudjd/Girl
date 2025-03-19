from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
import edge_tts
import asyncio
import uvicorn
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Initialize TTS Model (Coqui AI)

# Request Model
class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "Flirty AI is Live!"}

@app.post("/chat")
async def chat_ai(request: ChatRequest):
    user_input = request.user_input
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)
    
    reply = response.text
    return {"reply": reply}


@app.post("/speak")
async def speak_ai(request: ChatRequest):
    text = request.user_input
    audio_path = "voice_output.mp3"

    # Generate AI voice using Edge-TTS
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(audio_path)

    return {"audio_url": f"http://localhost:8000/{audio_path}"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
