import requests
import json
import os
import asyncio
from typing import Any, Optional
from pydantic import BaseModel, Field
from dotenv import find_dotenv, load_dotenv
from agents import  function_tool

load_dotenv(find_dotenv())
MAP_API_KEY =os.getenv('GOOGLE_MAPS_API_KEY')

PLACES_URL='https://places.googleapis.com/v1/places:searchNearby'

class Places(BaseModel):
    name:str
    address:str
    rating: Optional[float] = Field(default=None)
    
@function_tool
async def get_nearby_places(ctx, lat:float,lng:float):
    """Find nearby clinics or hospitals using Google Places API.
    Args:
        lat: Latitude of the search center.
        lng: Longitude of the search center.
    """
    
    key = MAP_API_KEY
    if not key:
        raise ValueError('Google map API key not valid or found.')
    
    print('places location\n',lat, lng)
    
    payload = {
        "includedTypes": ["apartment_building",'housing_complex','apartment_complex','lodging','cottage'],
        "maxResultCount": 3,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": 1000.0
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id,places.rating"
    }
    
    try:    
        response = requests.post(PLACES_URL,json=payload,headers=headers)
        output_data=response.json()
        print('repsonse:',response)
        
        if not output_data.get('places'):
            return json.dumps({'status':404, 'message':'Results not found'})
        
        # RESPONSE FORMATING
        results =[]
        for data in output_data.get('places',[]):
            place = Places(
                name=data.get('displayName',{}).get('text',''),
                address=data.get('formattedAddress'),
                rating=data.get('rating')
            )
            results.append(place.model_dump())
            
        print('nearby places',results)
        return json.dumps({"count": len(results), "results": results})
    except Exception as e:
        print('Exception: ',e)
        
        
# if __name__ == "__main__":
#     asyncio.run(get_nearby_places(24.917218,67.0923866))