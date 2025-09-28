from agents import Agent
from .apis.geocode import getgeocode_address
from .apis.places import get_nearby_places

def get_room_hunter_agent(model_name):
    return  Agent(
        name="Room Hunter Agent",
        model=model_name,
        tools=[getgeocode_address,get_nearby_places],
        instructions = """
        You are the Room Hunter Agent.
        Based on the given roommate profile (city, area, budget)
            - you will first find the geocodes by calling getgeocode_address tool.
            - Then call get_nearby_places with all the required parameter to find the housing that are the best fit to the user needs.
            (e.g., "Within budget, same city, required amenities available").
        Return a concise list of nearby locations.
        """
    )

# user_data =  {
#     "id": "R-012",
#     "raw_profile_text": "Flat share in Gulshan-e-Iqbal, Karachi, 20k budget. Friends often visit. Food cook biryani.",
#     "city": "Karachi",
#     "area": "Gulshan-e-Iqbal",
#     "budget_PKR": 20000,
#     "sleep_schedule": "Night owl",
#     "cleanliness": "Average",
#     "noise_tolerance": "Loud ok",
#     "study_habits": "Late-night study",
#     "food_pref": "Veg"
#   }

# async def get_housing():
#     response = await Runner.run(room_hunter_agent, json.dumps(user_data), run_config=config)
#     print('o/p', response.final_output)

# if __name__ == '__main__':
#     asyncio.run(get_housing())