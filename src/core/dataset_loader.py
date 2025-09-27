from agents import Runner, function_tool, Agent
import json
import asyncio
from setup_config import config
import os

@function_tool
def load_profiles():
    # Construct the file path relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "pakistan_roommate_profile.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

datareader = Agent(
    name='Profiles Reader agent',
    instructions="""
    You will use the load_profiles tool and give me the list of profile whose budget_PKR is 8000
    """,
    tools=[load_profiles]
)

async def main():
    result = await Runner.run(datareader, 'Hi, filter the profiles based on the given conditions' ,run_config=config)
    output=result.final_output
    print(output)

if __name__ == '__main__':
    asyncio.run(main())