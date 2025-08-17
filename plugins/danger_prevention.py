# plugins/danger_prevention.py

import os
import httpx
import re
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class DangerPreventionPlugin:
    def __init__(self, default_country="us"):
        self.hotlines = {
            "us": "1-800-273-TALK (8255)",
            "ca": "1-833-456-4566",
            "uk": "116 123",
            "default": (
                "If you're in crisis, please reach out to a local mental health hotline in your country. "
                "You are not alone, and help is available."
            )
        }
        self.default_country = default_country
        self.triggers = [
            "kill myself", "suicide", "end it all", 
            "i want to die", "i hate my life", "life is meaningless"
        ]

    def detect(self, message: str) -> bool:
        cleaned = re.sub(r"[^\w\s]", "", message.lower())
        return any(trigger in cleaned for trigger in self.triggers)

    async def respond(self, user_message: str) -> str:
        hotline = self.hotlines.get(self.default_country, self.hotlines["default"])
        system_prompt = (
            f"You are a compassionate crisis prevention AI. If a user expresses suicidal thoughts, "
            f"respond with urgency, empathy, and provide the following hotline number: {hotline}. "
            f"Encourage them to seek human help immediately."
        )

        payload = {
            "model": "openai/gpt-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return "Please talk to someone you trust. You're not alone. A local crisis line can help."

        except Exception as e:
            return f"Something went wrong. Please call a crisis line near you or reach out to a trusted person."