from agents import Runner, function_tool, Agent
import asyncio, json
from setup_config import config
from pydantic import BaseModel
from typing import Optional,Dict


class WingmanExplanation(BaseModel):
    candidate_id: str
    explanation_text: str
    suggestions: Optional[str] = None


@function_tool
def analyze_profiles(input_data: dict) -> dict:
    """
    Simple rule-based analyzer for Wingman Agent.
    Takes input_data: {user_profile, candidate_profile, match_score, conflicts}
    Returns structured dict with candidate_id, positives, conflicts, raw_suggestions.
    """
    try:
        candidate_id = input_data.get("candidate_profile", {}).get("id", "unknown")
        user_city = input_data.get("user_profile", {}).get("city")
        candidate_city = input_data.get("candidate_profile", {}).get("city")
        score = input_data.get("match_score", {}).get("score", 0)
        reasons = input_data.get("match_score", {}).get("reasons", [])
        conflicts = input_data.get("conflicts", [])

        positives = []
        if user_city and candidate_city and user_city == candidate_city:
            positives.append(f"Both live in {user_city}")
        if reasons:
            positives.extend([r for r in reasons if "mismatch" not in r.lower()])

        raw_suggestions = None
        if any("budget mismatch" in c.lower() for c in conflicts):
            raw_suggestions = "Discuss rent sharing or adjust budget expectations."
        elif any("sleep routine" in c.lower() for c in conflicts):
            raw_suggestions = "Agree on quiet hours or compromise sleep schedules."
        else:
            raw_suggestions = "Compatibility looks good, minor issues only."

        return {
            "candidate_id": candidate_id,
            "positives": positives,
            "conflicts": conflicts,
            "raw_suggestions": raw_suggestions
        }
    except Exception as e:
        return {
            "candidate_id": "unknown",
            "positives": [],
            "conflicts": [],
            "raw_suggestions": f"Error: {str(e)}"
        }

wingman_agent = Agent(
    name="Wingman Agent",
    instructions="""
    You are the Wingman Agent.
    - Always call the `analyze_profiles` tool with the input JSON.
    - Take the tool output and rewrite it into final JSON in this schema:
      { "candidate_id": str, "explanation_text": str, "suggestions": str }
    - explanation_text must be in natural language (English/Urdu mix allowed),
      combining positives and conflicts.
    - suggestions must be one compromise idea or confirmation.
    """,
    tools=[analyze_profiles],
    output_type=WingmanExplanation
)

example_input = {
    "user_profile": {
        "id": "R-007",
        "city": "Multan",
        "budget_PKR": 9000,
        "sleep_schedule": "Flexible"
    },
    "candidate_profile": {
        "id": "R-005",
        "city": "Multan",
        "budget_PKR": 20000,
        "sleep_schedule": "Night owl"
    },
    "match_score": {
        "score": 6,
        "reasons": ["Same city", "Both tidy", "Quiet environment", "Budget mismatch", "Different sleep schedule"]
    },
    "conflicts": ["Budget mismatch: 9k vs 20k", "Sleep routine mismatch"]
}


async def run_wingman():
    result = await Runner.run(
        wingman_agent,
        input=[json.dumps(example_input)],
        run_config=config
    )
    print(result.final_output.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(run_wingman())
