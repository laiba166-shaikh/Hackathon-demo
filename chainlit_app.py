import chainlit as cl
import json
from src.core.orchestrator import smart_student_living

@cl.on_chat_start
async def start():
    await cl.Message(
        content="**Smart Student Living - Find your Compatible Room mate**\n\nPlease enter your rental ad (e.g., 'Karachi Gulshan e Iqbal near Nipa. Budget 38k. Saaf sutra banda chahiye. Raat ko 10 baje so jata hoon. Non-veg khata hoon. Bilkul shor pasand nahi. Guests allowed nahi.')"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    try:
        result = await smart_student_living(user_input)
        if isinstance(result, dict):
            user_profile = result.get("user_profile", {})
            top_matches = result.get("top_matches", [])

            user_profile_str = "\n".join([
                f"**{k.replace('_', ' ').title()}**: {v}" for k, v in user_profile.items()
            ])

            matches_str = ""
            for idx, match in enumerate(top_matches, 1):
                profile = match.get("profile", {})
                score = match.get("score", {})
                red_flags = match.get("red_flags", [])
                suggestions = match.get("suggestions", "")

                profile_str = "\n".join([
                    f"{k.replace('_', ' ').title()}: {v}" for k, v in profile.items()
                ])
                score_str = f"Score: {score.get('match_score', '-')}, Reasons: {score.get('reasons', '-') }"
                red_flags_str = "\n- ".join(red_flags) if red_flags else "None"

                matches_str += f"\n---\n**Match #{idx}**\n{profile_str}\n{score_str}\n**Red Flags:**\n- {red_flags_str}\n**Suggestions:** {suggestions}\n"

            final_msg = f"**Your Profile:**\n{user_profile_str}\n\n**Top Matches:**{matches_str}"
            await cl.Message(content=final_msg).send()
        else:
            await cl.Message(content=f"**Result:**\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
