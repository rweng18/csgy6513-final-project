import os, csv, json, asyncio
from dotenv import load_dotenv, dotenv_values
from collections import defaultdict
from google.type import latlng_pb2 #used to calculate the center point of the circle search
from google.maps import places_v1
from google.protobuf.json_format import MessageToDict



#load .env file from current directory and test API key (not in venv)
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")
#print(api_key)

async def proximity_search(latLng, category): #coordinates should be a tuple, category should be a string
  
    #set up client, feed in API key as the argument
    client = places_v1.PlacesAsyncClient(
        client_options = {"api_key": api_key})
  
    # Define the latitude and longitude from the passed argument
    lat = latLng[0]
    lng = latLng[1]

    #define the radius which will be static 
    radius_meters = 1609 #approximately 1 miles
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
        included_types=[category],
        rank_preference=places_v1.SearchNearbyRequest.RankPreference.DISTANCE,
    )
    # Set the field mask
    fieldMask = "places.formattedAddress,places.displayName,places.location"

    # Make the request
    response = await client.search_nearby(request=request, metadata=[("x-goog-fieldmask",fieldMask)])

    return response


#test print of the returned object (probably a json)
async def main():

    #for every lat and long coordinate we have (each subway station), we'll make a query for every category
    locations = {} #create a dictionary for conversion to json later
    categories = ["art_gallery", "art_studio", "auditorium", "cultural_landmark", "historical_place", "monument", "museum", "performing_arts_theater", "sculpture"]

    #populate locations from .csv
    stations_file_path = ".\station_by_line_noRoutes.csv"
    with open(stations_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) #skip header

        for row in reader:
            coordinates = (float(row[1]), float(row[2]))
            locations[row[0]] = {"Coordinates": coordinates} #use the name of the subway station as the top-level

    #run a search in places API for every location we have against every category
    for name, data in locations.items():
        stopName = name
        latLng = data["Coordinates"]
        for category in categories:
            data = await proximity_search(latLng, category)
            #serializedData = MessageToDict(data._pb, preserving_proto_field_name=True)  #searchNearBy response is wrapped as proto-plus object.  directly access the ._pb gives us the protobuf object to convert to dict
            #file_path = ".\outputFile"
            #with open(file_path, 'w') as outputFile:
            #json.dump(serializedData, outputFile, indent = 3)

if __name__ == "__main__":
    asyncio.run(main())        