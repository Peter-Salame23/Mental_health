# agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from medical_check import validate_response

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MentalHealthAgent:
    def __init__(self):
        pass

    def run(self, user_message: str) -> str:
        prompt = f"""
You are a compassionate mental health support assistant focused on helping men express emotional and psychological struggles.

Instructions:
- Use active listening and supportive language.
- Encourage users to keep talking about their feelings.
- If a user says they are feeling unwell, or have any negative emotions, ask them why and offer advice
- If a user says they are sad, ask why they are sad and then offer advice on how to deal with it

Now continue the conversation:

User: {user_message}
Assistant:"""

        try:
            # Generate response from GPT-4
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a supportive and empathetic mental health assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            reply = response.choices[0].message.content.strip()

            # Check the response for any risk triggers
            check = validate_response(reply)

            if "⚠️" in check:
                return f"{check}\n\n[Filtered reply:]\n{reply}"

            return reply

        except Exception as e:
            return f"❌ API error: {str(e)}"
