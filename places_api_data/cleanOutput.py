import os, csv, json, asyncio
from dotenv import load_dotenv, dotenv_values
from collections import defaultdict
from google.type import latlng_pb2 #used to calculate the center point of the circle search
from google.maps import places_v1
from google.protobuf.json_format import MessageToDict

import json

#Read existing file from testRequest.py
with open("outputFile.json", "r") as f:
    original_data = json.load(f)

# Convert to list of flattened dicts

#create empty container
json_lines = []

#for every object, create a flat line per object then append it to the new list of dictionaries
for name, data in original_data.items():
    flattened = {"name": name}
    flattened.update(data)
    json_lines.append(flattened)

# Write as newline-delimited JSON (JSONL)
with open("outputFile_converted.json", "w") as f:
    f.write("[")
    for i, entry in enumerate(json_lines):
        if i != len(json_lines)-1:
            f.write(json.dumps(entry) + ",")
        else:
            f.write(json.dumps(entry) + "]") 