from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

from plugins.danger_prevention import DangerPreventionPlugin

# Load keys
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Init app & plugin
app = FastAPI()
danger_plugin = DangerPreventionPlugin(default_country="us")

class UserInput(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Mental Health Agent is running."}

@app.post("/chat")
async def chat(user_input: UserInput):
    user_message = user_input.message

    # 🔌 Check for danger signals
    if danger_plugin.detect(user_input.message):
        print("🚨Danger prevention plugin triggered")
        reply = await danger_plugin.respond(user_input.message)
        hotline = danger_plugin.hotlines.get(danger_plugin.default_country, danger_plugin.hotlines["default"])
        return {"response": f"{reply} {hotline}"}

    # 🧠 System prompt setup
    system_prompt = (
        "You are a supportive mental health agent. Engage the user with kindness, and provide informational support if appropriate. "
        "Avoid medical claims or diagnosis. Be a helpful listener."
    )

    payload = {
        "model": "anthropic/claude-3-sonnet",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input.message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

    if response.status_code != 200:
        return {"response": "Sorry, something went wrong while generating a response."}

    reply = response.json()["choices"][0]["message"]["content"]
    return {"response": reply}