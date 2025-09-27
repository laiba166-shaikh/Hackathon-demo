# from setup_config import config
from pydantic import BaseModel
from agents import Agent

class RedFlags(BaseModel):
    conflicts: list[str]

# @function_tool
# def get_user_profiles():
#     return [{
#     "id": "R-001",
#     "raw_profile_text": "Hostel seat available G-11, Islamabad. Budget no issue. Want Tidy banda, prefer Online classes, Quiet ok.",
#     "city": "Islamabad",
#     "area": "G-11",
#     "budget_PKR": 13000,
#     "sleep_schedule": "Night owl",
#     "cleanliness": "Tidy",
#     "noise_tolerance": "Quiet",
#     "study_habits": "Online classes",
#     "food_pref": "Flexible"
#   },
#   {
#     "id": "R-002",
#     "raw_profile_text": "Hostel seat available Gulshan-e-Iqbal, Karachi. Budget no issue. Want Messy banda, prefer Late-night study, Quiet ok.",
#     "city": "Karachi",
#     "area": "Gulshan-e-Iqbal",
#     "budget_PKR": 14000,
#     "sleep_schedule": "Night owl",
#     "cleanliness": "Messy",
#     "noise_tolerance": "Quiet",
#     "study_habits": "Late-night study",
#     "food_pref": "Flexible"
#   }]

def get_redflag_agent(model_name):
  return Agent(
      name="Red Flag Agent",
      model=model_name,
      instructions="""
      You are the Red Flag Agent in a roommate matching system.

      You are 
      Each profile has attributes like: city, budget_pkr, cleanliness, sleep_schedule, 
      noise_tolerance, study_habits, food_pref, guests_policy, smoking_ok, gender, notes.

      Your task: **Detect lifestyle conflicts or dealbreakers** between the two profiles.  

      Guidelines:
      - Compare each field logically.
      - If the values are compatible or not specified, do not report anything.
      - If there is a mismatch, output a short conflict statement.

      Examples of conflicts:
      - "City mismatch: Lahore vs Karachi"
      - "Budget gap more than 15k PKR"
      - "Sleep schedule clash: early bird vs night owl"
      - "Noise mismatch: one prefers quiet, other tolerates high noise"
      - "Guests mismatch: one allows friends, other wants no guests"
      - "Smoking mismatch: one smokes, other does not"
      
      Each conflict must be a short, clear sentence.
      """,
      output_type=RedFlags,
    ) 