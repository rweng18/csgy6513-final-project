import os
import json
import asyncio
from dotenv import load_dotenv, dotenv_values
from google.type import latlng_pb2 #used to calculate the center point of the circle search
from google.maps import places_v1
from google.protobuf.json_format import MessageToDict



#load .env file from current directory and test API key (not in venv)
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
#print(api_key)

async def proximity_search():
  
    #set up client, feed in API key as the argument
    client = places_v1.PlacesAsyncClient(
        client_options = {"api_key": api_key})
  
    # Define the coordinates and radius
    lat = 40.692999 
    lng = -73.925389
    radius_meters = 16093 #approximately 10 miles
    # Create the LatLng object for the center
    center_point = latlng_pb2.LatLng(latitude=lat, longitude=lng)
    # Create the circle
    circle_area = places_v1.types.Circle(
        center=center_point,
        radius=radius_meters
    )
    # Add the circle to the location restriction
    location_restriction = places_v1.SearchNearbyRequest.LocationRestriction(
        circle=circle_area
    )
    # Build the request
    request = places_v1.SearchNearbyRequest(
        location_restriction=location_restriction,
        included_types=["art_gallery", "art_studio", "auditorium", "cultural_landmark", "historical_place", "monument", "museum", "performing_arts_theater", "sculpture"]
    )
    # Set the field mask
    fieldMask = "places.formattedAddress,places.displayName,places.location"
    # Make the request
    response = await client.search_nearby(request=request, metadata=[("x-goog-fieldmask",fieldMask)])
    return response


#test print of the returned object (probably a json)
async def main():
    data = await proximity_search()
    serializedData = MessageToDict(data._pb, preserving_proto_field_name=True)  #searchNearBy response is wrapped as proto-plus object.  directly access the ._pb gives us the protobuf object to convert to dict
    file_path = ".\outputFile"
    with open(file_path, 'w') as outputFile:
        json.dump(serializedData, outputFile, indent = 3)

if __name__ == "__main__":
    asyncio.run(main())        