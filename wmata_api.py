import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "aab3368d715f470eac329e0831e62957" # https://developer.wmata.com/demokey
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# Retrieve incidents by unit type
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    unit_type = unit_type.upper() 
    
    # create an empty list called 'incidents'
    incidents = []


    # use 'requests' to do a GET request to the WMATA Incidents API
    response = requests.get(INCIDENTS_URL, headers=headers)
    
    # retrieve the JSON from the response
    json_response = response.json()
    
    # iterate through the JSON response and retrieve all incidents 
    # matching 'unit_type'
    for incident in json_response.get("ElevatorIncidents", []):
        
        # for each incident, create a dictionary containing the 
        # 4 fields from the Module 7 API definition
        if incident.get("UnitType") == unit_type:
            
            # add each incident dictionary object to the 'incidents' list
            incidents.append({
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitName": incident.get("UnitName"),
                "UnitType": incident.get("UnitType")
            })
    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)


if __name__ == '__main__':
    app.run(debug=True)
