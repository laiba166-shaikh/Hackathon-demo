from agents import Agent
from dataset_loader import load_house_listing

room_hunter_agent = Agent(
    name="Room Hunter Agent",
    instructions = """
    You are the Room Hunter Agent.
    First, use the `load_house_listing` tool to fetch all available housing listings.
    Then, based on the given roommate profile (city, area, budget, required rooms, amenities),
    analyze the listings yourself and select the top 3 best matches.

    Do not just return raw data — you must perform the matching logic.
    For each recommended room, explain briefly why it is a good fit 
    (e.g., "Within budget, same city, required amenities available").
    """,
    tools=[load_house_listing]
)