Pipeline notes:  *NOTES ARE FROM A DUMP FROM WORKING SESSION - NOT ALL ACCURATE TO FINAL PROTOTYPE*

1.  Set up Google Cloud Projects: provides API keys for HTTP requests to retrice places data
2.  Write a program to pull and create data set from Google places API.
    Google place requests from the API all take in HTTP requests (structure: https://google.aip.dev/127), similar to computer networking
    Program should define a message and listen for a reply  with the JSON structure we need.
    https://developers.google.com/maps/documentation/places/web-service/reference/rest/v1/places
    It is easier to use cloud client libraries to call the places API:  https://cloud.google.com/apis/docs/cloud-client-libraries
    Python Client library supports calling the places API: https://github.com/googleapis/google-cloud-python
    Specific library: https://github.com/googleapis/google-cloud-python/tree/main/packages/google-maps-places
    C++ does not support places API:  https://github.com/googleapis/google-cloud-cpp
3.  Program exports dataset locally (but we can add functionaliaty to directly upload to a database in the future)


Examples:
https://github.com/googleapis/google-cloud-python
https://developers.google.com/maps/documentation/places/web-service/client-library-examples#python

Installing (after you're in venv)

https://developers.google.com/maps/documentation/places/web-service/client-libraries#python

Setting up authentication default credentials:
https://cloud.google.com/docs/authentication/provide-credentials-adc

Since I'm running in venv, use the local development environment steps:
https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment

First install the gcloud CLI (NOT IN VENV)
https://cloud.google.com/sdk/docs/install

Log in with google cloud.

Success page: https://cloud.google.com/sdk/auth_success
gcloud CLI: https://cloud.google.com/sdk/gcloud
use gcloud shell to use the correct cloud project ID

Authenticating with client libraries: 
https://cloud.google.com/docs/authentication/client-libraries?_gl=1*epbx06*_ga*MzI4MjQ1MDMyLjE3NTI0NzEwMTc.*_ga_NRWSTWS78N*czE3NTI5NDE5MTUkbzMkZzEkdDE3NTI5NDM5NzgkajQyJGwwJGgw


First, go through the client library example to see how you would authenticate: https://developers.google.com/maps/documentation/places/web-service/client-library-examples

Start writing .py program outside of venv.
Ensure the interpreter as the one from the venv by locating it in \Scripts so that importing from google.maps doesn't throw a error/warning

Set up a .env file in the root category and add to .gitignore (API key lives here)
install python-dotenv to pull key for this file

Do a coordinate nearby search by proximity or define a circle location bias fusing a dictionary.

Use nearbySearch:
https://developers.google.com/maps/documentation/places/web-service/nearby-search

(must include fields to return or the method will return an error):
https://developers.google.com/maps/documentation/places/web-service/choose-fields)

then also include: optional paramters to include a list of types from table A: https://developers.google.com/maps/documentation/places/web-service/place-types#table-a

Table B cannot be used a filter, but can be extracted from the response.

Pipeline likely will get a list of all json objects that are within the region circle, then further filter down json objects by address zip codes in NYC.

Turns out the center of the city is a hotly debated topic, but I decided on an approximate center:
https://www.google.com/maps/place/40%C2%B041'34.8%22N+73%C2%B055'31.4%22W/@40.718377,-74.0388147,10.81z/data=!4m4!3m3!8m2!3d40.693!4d-73.9254?entry=ttu&g_ep=EgoyMDI1MDcyMC4wIKXMDSoASAFQAw%3D%3D

We'll go 1 miles out from 40°41'34.8"N 73°55'31.4"W

Those coordinates need to be converted into decimal degrees instead.... https://www.fcc.gov/media/radio/dms-decimal

Latitude: 40°41'34.8"N
Degrees = 40
Minutes = 41
Seconds = 34.8
Decimal = 40 + (41 / 60) + (34.8 / 3600) ≈ 40.692999

Longitude: 73°55'31.4"W

Degrees = 73
Minutes = 55
Seconds = 31.4
Decimal = 73 + (55 / 60) + (31.4 / 3600) ≈ 73.925389
Since it's W, it's negative → −73.925389

Python client for the Cloud Places API, and the object returned (SearchNearbyResponse) is a protocol buffer (protobuf) object, not raw JSON.
https://googleapis.dev/python/protobuf/latest/google/protobuf/json_format.html

RESEARCH - not sure why the python client library would return a protobuf object instead of just the json, will look into this.

returned object need to be serialized into JSON directly

turns out google places API only allow up to 60  entries to be returned and requires pagination, and full data is not available without commercial agreements.
The python client library does not provide next_page tokens for nearbySearch, which limits us to 20 entries (for one page)
We'll need to chunk out the queries for every subway station and change our scorecard to consider 20+ return results as the maximum score for that category.
We can also chunk out each query for every type.

New process:

In jupyter notebooks, Reduce station_by_line by unique stations only (we'll separate the routes out in the rejoin later)

Search within a mile radius of every subway station from station_by_line.csv
rank preference by distance

