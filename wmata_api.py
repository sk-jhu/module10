import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "aab3368d715f470eac329e0831e62957" # https://developer.wmata.com/demokey
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    unit_type = unit_type.upper()  # Convert to match WMATA data
    incidents = []

    try:
        response = requests.get(INCIDENTS_URL, headers=headers)
        response.raise_for_status()
        json_response = response.json()
    except requests.RequestException as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}

    for incident in json_response.get("ElevatorIncidents", []):
        if incident.get("UnitType") == unit_type:
            incidents.append({
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitName": incident.get("UnitName"),
                "UnitType": incident.get("UnitType")
            })

    return json.dumps(incidents), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
