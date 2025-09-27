import os
import asyncio
from setup_config import config
from agents import Agent, Runner, set_default_openai_api, set_tracing_disabled
   
set_default_openai_api('chat_completions')
set_tracing_disabled(True)

async def ask_agent(userMessage:str):
    agent = Agent(
        name='Assistant', 
        instructions='You are a helpful assistant.',
    )

    result = await Runner.run(agent, userMessage,run_config=config)
    output=result.final_output
    print(output)
    return output
    
if __name__ == "__main__":
    asyncio.run(ask_agent('How are you?'))