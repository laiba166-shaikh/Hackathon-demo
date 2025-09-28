import os
from dotenv import load_dotenv, find_dotenv
# from setup_config import config
import asyncio
import json
from pydantic import BaseModel
from typing import Optional
from .profile_reader_agent import get_profile_reader_agent
from .match_scorer_agent import get_match_scorer_agent
from .redflag_agent import get_redflag_agent
from .wingman_agent import get_wingman_agent
from .room_matcher_agent import get_room_hunter_agent
from agents import Agent, Runner,OpenAIChatCompletionsModel, RunConfig,AsyncOpenAI, ModelProvider, Model, set_default_openai_api, set_tracing_disabled, set_default_openai_client

load_dotenv(find_dotenv())

set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

async def set_fallback_llm():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    print('gemini key',GEMINI_API_KEY)
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta",
    )
    set_default_openai_client(client=external_client, use_for_tracing=False)


def load_profiles():
    # Construct the file path relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "pakistan_roommate_profile.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

async def smart_student_living(user_input:str, degrade:bool=False):
    roommates_data= load_profiles()
    
    # Adjust paramteres if Degrade mode
    if degrade:
        await set_fallback_llm()
                
    MODEL_NAME='gemini-2.0-flash' if degrade else 'gpt-4.1-mini'
    print('degrade: ',degrade, MODEL_NAME) 
    
    room_hunter_agent = get_room_hunter_agent(MODEL_NAME)
    profile_reader = get_profile_reader_agent(MODEL_NAME)
    match_scorer = get_match_scorer_agent(MODEL_NAME)
    detect_conflicts = get_redflag_agent(MODEL_NAME)
    wingman_agent= get_wingman_agent(MODEL_NAME)
    
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
            1a. If user just ask about the location handsoff it to the room_hunter_agent.
            
            2. For each dataset profile:
                - Call "score_match" to compute compatibility score.
                - Call "detect_conflicts" to find red flags.
                - Call "explain_match" to generate a short explanation.
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
                    "suggestions": { ... }
                },
                ...
            ]
            }
                       
        """,
        tools=[
            profile_reader.as_tool(tool_name="parse_user_profile",tool_description="Parse User_ad into a clean structured format"),
            match_scorer.as_tool(tool_name='score_match',tool_description="Compare the user profile data with the dataset profile and returns the match score and resons."),
            detect_conflicts.as_tool(tool_name='detect_conflicts',tool_description="Compare the user profile data with the dataset profile and returns a list of conflicts in a short and clear sentence."),
            wingman_agent.as_tool(tool_name="explain_match",tool_description="Consider the matching score and conflicts and return summary and suggestions based on the profiles data.")
        ],
        tool_use_behavior="stop_on_first_tool" if degrade else "run_llm_again",
        handoffs=[room_hunter_agent],
        handoff_description='Look at the address, area and city of the user and hand over to room_hunter_agent only if user ask to provide him the nearby places.',
    )
    
    user_prompt = json.dumps({
        'User_ad': user_input,
        "Roommate_dataset":roommates_data,  
    })
    
    try:
        response = await Runner.run(orch, user_prompt)
        output = response.final_output
        print('output: ',output)
        return output
    except Exception as e:
        print('error: ', e)
        return 'None'

if __name__ == "__main__":
    # user_raw_ad = "Karachi Gulshan e Iqbal near Nipa. Budget 38k. Saaf sutra banda chahiye. Raat ko 10 baje so jata hoon. Non-veg khata hoon. Bilkul shor pasand nahi. Guests allowed nahi."
    user_asking_loc ="Hostel seat available G-11, Islamabad. Budget no issue. Want Tidy banda, prefer Online classes, Quiet ok.I just want to know the nearby housing information."
    asyncio.run(smart_student_living(user_asking_loc, degrade=True))