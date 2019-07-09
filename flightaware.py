#!/usr/bin/python3
import requests
import json
#import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time
import textwrap


from flightawarelib.arrived import FlightAwareArrived
from flightawarelib.departed import FlightAwareDeparted
from flightawarelib.enroute import FlightAwareEnroute
from flightawarelib.metar import Metar
from flightawarelib.metar import MetarEx


"""
REST / JSON

FlightXML 2.0 can also be accessed using a light-weight "Representational state transfer" (REST) inspired protocol that
returns its responses encoded in "JavaScript Object Notation" (JSON) format.
This allows FlightXML to be used in environments in which it is inconvenient or impossible to invoke SOAP services,
such as mobile phone applications, web browser applications, or server-side JavaScript environments.

To access any method, simply perform either a GET or POST request
to http://flightxml.flightaware.com/json/FlightXML2/METHODNAME using standard CGI-style representation of the arguments.
All requests made must supply the username and API Key as a "basic" Authorization HTTP header.

For example, the following URL is how you might request the current weather at
John F. Kennedy airport (KJFK) in New York:
http://flightxml.flightaware.com/json/FlightXML2/MetarEx?airport=KJFK&startTime=0&howMany=1&offset=0

Requests can be returned in "JSONP" format, allowing a web page to load the response in a way that avoids the same-domain
security restrictions enforced by some browsers. To do this, simply specify the
optional argument "jsonp_callback" with a value that is the name of the
JavaScript function that should be invoked with the JSON data.
"""

airport = "KAMA"
queryfilter = "airline"


# print eighty lines of whatever character is passed
def printeighty(what):
    for i in range(80):
        if i < 79:
            print(what, end='')
        else:
            print(what, end='\n', flush=True)


# MAIN PROGRAM
# use metar
metar = Metar()
metar_result = metar.get_flightaware_metar(airport)
print(metar_result)

# use metarx
metarex = MetarEx()
json_result = metarex.get_flightaware_metarex_json(airport, int(time.mktime(datetime.now().timetuple())))
formatted = metarex.print_flightaware_metarex_from_json(json_result)
print(formatted)

# call Arrivals
arrived = FlightAwareArrived()
print("ARRIVALS to " + airport)
printeighty("*")

arrivals = arrived.get_flightaware_arrived(airport, queryfilter, 10, 0)
arrived.print_flightaware_arrived(arrivals)
arrived.write_flightaware_arrivals_to_db(arrivals)

# call Departures
departed = FlightAwareDeparted()
print("DEPARTURES from " + airport)
printeighty("*")

departures = departed.get_flightaware_departed(airport, queryfilter, 10, 0)
departed.print_flightaware_departed(departures)
departed.write_flightaware_departures_to_db(departures)

# call Enroutes
departed = FlightAwareEnroute()
print("ENROUTE to or from " + airport)
printeighty("*")

enroutes = departed.get_flightaware_enroute(airport, queryfilter, 10, 0)
departed.print_flightaware_enroute(enroutes)
departed.write_flightaware_enroutes_to_db(enroutes)
