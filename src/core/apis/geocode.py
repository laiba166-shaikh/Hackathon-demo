import requests
import json
import os
import asyncio
from typing import Any
from pydantic import BaseModel
from dotenv import find_dotenv, load_dotenv
from agents import RunContextWrapper, function_tool

load_dotenv(find_dotenv())
MAP_API_KEY =os.getenv('GOOGLE_MAPS_API_KEY')

GEOCODE_URL= "https://maps.googleapis.com/maps/api/geocode/json"

class UserLocation(BaseModel):
    address:str
    lat:float
    lng:float
    place_id:str

@function_tool
async def getgeocode_address(ctx, address:str)->str:
    """Turn a human readable address or area name into latitude and longitude.
    Args:
        address: Free text such as "Model Town Lahore" or a full street address.
    """
    
    key = MAP_API_KEY
    if not key:
        raise ValueError('Google map API key not valid or found.')

    print('geocode address:', address)
    params = {
        'address':address,
        'key':key
    }
    try:    
        response = requests.get(GEOCODE_URL,params)
        output_data=response.json()
        
        # ZERO RESULTS or ERROR
        status = output_data.get('status')
        if not status in {'OK', 'ZERO_RESULTS'}:
            error_message = output_data.get('error_message')
            raise RuntimeError('Google Map Error', error_message or status)
        
        if status == 'ZERO_RESULTS' or not output_data.get('results'):
            return json.dumps({'status':404, 'message':'Results not found'})
        
        # RESPONSE FORMATING
        result = output_data.get('results')[0]
        location =result['geometry']['location']
        user_location = UserLocation(
            address= result.get('formatted_address'),
            place_id=result.get('place_id'),
            lat=location.get('lat'),
            lng=location.get('lng')
        )
        print('geocode data:', user_location)
        return json.dumps(user_location.model_dump())
    except Exception as e:
        print('Exception: ',e)
        return 'Geocode data not found.'
        
        
# if __name__ == "__main__":
#     user_location=input('Please enter your location to find the nearby hospital:\n')
#     asyncio.run(getgeocode_address(user_location))