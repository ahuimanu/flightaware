import json
import requests
from requests.auth import HTTPBasicAuth

base_url = "http://flightxml.flightaware.com/json/FlightXML2/"

user = 'ahuimanu'
key = '4b2964bc3aaababdb43c5c3b1e9eefdd4ce0d598'

auth = HTTPBasicAuth(user, key)


def GetMetarText(airport):
    args = {'airport': airport, }
    req = requests.get(f"{base_url}Metar", auth=(user, key), params=args)
    return req.text


def FleetScheduled(fleet, howMany, offset):
    args = {
        'fleet':fleet,
        'howMany':howMany,
        'offset':offset,
    }
    req = requests.get(f"{base_url}FleetScheduled", auth=(user, key), params=args)
    resp = req.json()
    output = ""
    for flight in resp["FleetScheduledResult"]["scheduled"]:
        output += f"{flight['ident']}\n"

    return output


print(GetMetarText("KAMA"))
print(FleetScheduled("AAL", 15, 0))

# req2 = requests.get(f"{base_url}", auth=(user, key), params=args2)

