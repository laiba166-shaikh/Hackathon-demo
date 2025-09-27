# from setup_config import config
from pydantic import BaseModel
from agents import Agent

class MatchingResult(BaseModel):
    match_score: int 
    reasons: str

# @function_tool
# def get_user_profiles():
#     """"Return two Room mate profile to compare"""
#     return [
#         {
#             "id": "R-001",
#             "city": "Islamabad",
#             "area": "G-11",
#             "budget_PKR": 13000,
#             "sleep_schedule": "Night owl",
#             "cleanliness": "Tidy",
#             "noise_tolerance": "Quiet",
#             "study_habits": "Online classes",
#             "food_pref": "Flexible"
#         },
#         {
#             "id": "R-002",
#             "city": "Karachi",
#             "area": "Gulshan-e-Iqbal",
#             "budget_PKR": 14000,
#             "sleep_schedule": "Night owl",
#             "cleanliness": "Messy",
#             "noise_tolerance": "Quiet",
#             "study_habits": "Late-night study",
#             "food_pref": "Flexible"
#         }
#     ]

def get_match_scorer_agent(model_name)->Agent:
    return Agent(
        name="Match Score Agent",
        model=model_name,
        instructions="""
            You are a Match Scoring Agent. 
            Your responsibility is to evaluate the compatibility between two roommate profiles provided in the input and calculate a compatibility score (MATCH SCORE) on a scale of 0–10.

            Scoring Criteria:
            - Cleanliness: identical = +3, opposite = -3
            - Sleep schedule: identical = +2, different = 0
            - Noise tolerance: identical = +2, different = -2
            - Study habits: compatible/similar timing = +2, otherwise 0
            - Food preference: flexible = +1, mismatch = 0

            Rules:
            1. Use only the profiles given in the input. Do not assume missing details.
            2. Apply the scoring criteria strictly and transparently.
            3. Provide a concise reasoning for each scoring decision (e.g., "Both are tidy → +3").
            4. Return the final output strictly in JSON format according to the MatchingResult schema:
            {
                "match_score": <integer>,
                "reasons": "<string explanation>"
            }
            5. Do not include extra text, explanations, or formatting outside the JSON.
        """,
        output_type=MatchingResult
    )