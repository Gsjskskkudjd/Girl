from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import edge_tts
import asyncio
import uvicorn

# Initialize FastAPI
app = FastAPI()

# Fetch OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Request Model
class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "Flirty AI is Live!"}

@app.post("/chat")
async def chat_ai(request: ChatRequest):
    user_input = request.user_input

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" for cheaper requests
            messages=[{"role": "user", "content": user_input}]
        )

        return {"reply": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}

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
