import os
import asyncio
from setup_config import config
from agents import Agent, Runner, set_default_openai_api, set_tracing_disabled
from pydantic import BaseModel
from typing import Optional
import json
   
set_default_openai_api('chat_completions')
set_tracing_disabled(True)

class ProfileSchema(BaseModel):
    id: str
    raw_profile_text: str
    city: Optional[str] = None
    area: Optional[str] = None
    budget_PKR: Optional[int] = None
    sleep_schedule: Optional[str] = None
    cleanliness: Optional[str] = None
    noise_tolerance: Optional[str] = None
    study_habits: Optional[str] = None
    food_pref: Optional[str] = None
    guests_allowed: Optional[bool] = None

profile_Reader_agent=Agent(
    name="Profile Reader",
    instructions="""You are a Profile Reader Agent. 
Your task is to take a roommate advertisement written in mixed Urdu/English 
and convert it into a clean structured JSON format.  

Follow these rules:  
- Always return valid JSON only (no explanations, no extra text).  
- Extract as much information as possible, even if not all fields are present.  
- Normalize budget to an integer in PKR.  
- If any field is missing, put null.  
- Sleep schedule should be either: "Early sleeper" or "Night owl".  
- Cleanliness should be one of: "High", "Medium", "Low" or use synonyms like "Tidy".  
- Noise tolerance: "Quiet", "Moderate", "Noisy".  
- Food preference: "Veg", "Non-Veg", "Flexible".  
- Study habits: Short phrase (e.g., "Online classes", "Library study").  
- Area should be a sub-part of the city if mentioned.  
- Always include `id` in format: "R-###" where ### is a unique number you generate.  

### Example Input:
Karachi Gulshan e Iqbal near Nipa. Budget 38k. Saaf sutra banda chahiye. 
Raat ko 10 baje so jata hoon. Non-veg khata hoon. Bilkul shor pasand nahi. Guests allowed nahi.

### Example Output:
{
    "id": "R-002",
    "raw_profile_text": "Karachi Gulshan e Iqbal near Nipa. Budget 38k. Saaf sutra banda chahiye. Raat ko 10 baje so jata hoon. Non-veg khata hoon. Bilkul shor pasand nahi. Guests allowed nahi.",
    "city": "Karachi",
    "area": "Gulshan e Iqbal near Nipa",
    "budget_PKR": 38000,
    "sleep_schedule": "Early sleeper",
    "cleanliness": "High",
    "noise_tolerance": "Quiet",
    "study_habits": null,
    "food_pref": "Non-Veg",
    "guests_allowed": false
}

"""  ,
output_type=ProfileSchema)

async def main():
    user_input=input('Enter your Profile:')
    result=await Runner.run( profile_Reader_agent,input=user_input,run_config=config)
    print(result.final_output.model_dump_json(indent=2))
   
if __name__ == "__main__":
    asyncio.run(main())