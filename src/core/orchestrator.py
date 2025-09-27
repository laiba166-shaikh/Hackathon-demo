import os
from dotenv import load_dotenv, find_dotenv
# from setup_config import config
import asyncio
import json
from pydantic import BaseModel
from typing import Optional
from profile_reader_agent import get_profile_reader_agent
from match_scorer_agent import get_match_scorer_agent
from redflag_agent import get_redflag_agent
from agents import Agent, Runner,OpenAIChatCompletionsModel, RunConfig,AsyncOpenAI, ModelProvider, Model, set_default_openai_api, set_tracing_disabled, set_default_openai_client

# Load environment variables from .env file
load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print('gemini key',GEMINI_API_KEY)
MODEL_NAME='gemini-2.0-flash'

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta",
)

set_default_openai_client(client=external_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

# class CustomModelProvider(ModelProvider):
#     def get_model(self, model_name: str | None) -> Model:
#         return OpenAIChatCompletionsModel(model=model_name or MODEL_NAME, openai_client=external_client)

# CUSTOM_MODEL_PROVIDER = CustomModelProvider()

# run_config = RunConfig(model_provider=CUSTOM_MODEL_PROVIDER)

# async def ask_agent(userMessage:str):
#     agent = Agent(
#         name='Assistant', 
#         instructions='You are a helpful assistant.',
#     )

#     result = await Runner.run(agent, userMessage,run_config=config)
#     output=result.final_output
#     print(output)
#     return output

def load_profiles():
    # Construct the file path relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "pakistan_roommate_profile.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

async def main3():
    roommates_data= load_profiles()
    profile_reader = get_profile_reader_agent(MODEL_NAME)
    match_scorer = get_match_scorer_agent(MODEL_NAME)
    detect_conflicts = get_redflag_agent(MODEL_NAME)
    
    orch = Agent(
        name="Orchestrator",
        model=MODEL_NAME,
        instructions="""
            You are the Orchestrator for roommate matching.

            Input: 
            - A new roommate ad (raw text).
            - A dataset of profiles (JSON list).

            Steps you must follow:
            1. Parse the new ad with "parse_user_profile" tool.
            2. For each dataset profile:
                - Call score_match to compute compatibility score
                - Call "detect_conflicts" to find red flags.
            3. Collect results for all dataset profiles.
            4. Sort by score and return the TOP 3 matches.
            
            Output strictly as JSON:
            {
            "user_profile": { ... },
            "top_matches": [
                {
                    "profile": { ... },
                    "score": { ... },
                    "red_flags": { ... },
                },
                ...
            ]
            }
                       
        """,
        tools=[
            profile_reader.as_tool(tool_name="parse_user_profile",tool_description="Parse User_ad into a clean structured format"),
            match_scorer.as_tool(tool_name='score_match',tool_description="Compare the user profile data with the dataset profile and returns the match score and resons."),
            detect_conflicts.as_tool(tool_name='detect_conflicts',tool_description="Compare the user profile data with the dataset profile and returns a list of conflicts in a short and clear sentence.")
        ],
    )
    
    user_raw_ad = "Karachi Gulshan e Iqbal near Nipa. Budget 38k. Saaf sutra banda chahiye. Raat ko 10 baje so jata hoon. Non-veg khata hoon. Bilkul shor pasand nahi. Guests allowed nahi"
    user_prompt = json.dumps({
        'User_ad': user_raw_ad,
        "Roommate_dataset":roommates_data  
    })
    
    try:
        response = await Runner.run(orch,user_prompt)
        print(response.final_output)
    except Exception as e:
        print('error: ', e)


if __name__ == "__main__":
    asyncio.run(main3())