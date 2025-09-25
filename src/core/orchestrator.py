import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client, set_default_openai_api, set_tracing_disabled
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
BASE_URL=os.getenv('BASE_URL')
API_KEY=os.getenv('GEMINI_API_KEY')
MODEL='gemini-2.0-flash'

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

set_default_openai_api('chat_completions')
set_default_openai_client(client,use_for_tracing=False)
set_tracing_disabled(True)


async def ask_agent(userMessage:str):
    agent = Agent(name='Assistant', model=model, instructions='You are a helpful assistant.')

    result = await Runner.run(agent, userMessage)
    output=result.final_output
    return output
    
# if __name__ == "__main__":
#     asyncio.run(ask_agent('Hi'))