# chat_chainlit.py

import chainlit as cl
from agent import MentalHealthAgent

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("agent", MentalHealthAgent())
    await cl.Message(content=" Hello! This is your mental health assistant. How are you feeling today?").send()

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    try:
        response = agent.run(message.content)
    except Exception as e:
        response = f"❌ Error: {str(e)}"
    await cl.Message(content=response).send()
