import chainlit as cl
from core.orchestrator import ask_agent

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content=f"Hello, I am your helful Assistant. How can I help you today").send()
    

@cl.on_message
async def main(message:cl.Message):
    result = await ask_agent(message.content)
    await cl.Message(content=f"Received: {result}").send()
    