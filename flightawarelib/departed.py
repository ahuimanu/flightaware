#!/usr/bin/python3
import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

# FlightAwareDeparted class

# https://flightaware.com/commercial/flightxml/explorer/#op_Departed

# from FlightXML2 Explorer: Arrived returns information about flights that have recently arrived for the specified
# airport and maximum number of flights to be returned. Flights are returned from most to least recent. Only flights
# that arrived within the last 24 hours are considered.

# Times returned are seconds since 1970 (UNIX epoch seconds).


def get_flightaware_departures(airport, filterType, howMany, offset, user, key):
    # hold departures objects
    departures = []

    # Service URL
    url = "http://flightxml.flightaware.com/json/FlightXML2/Arrived?airport=" + airport + \
          "&filter=" + filterType + "&howMany=" + str(howMany) + "&offset=" + str(offset)

    # make request
    req = requests.get(url, auth=(user, key))

    # translate to JSON
    flightaware = req.json()

    for arrival in flightaware["ArrivedResult"]["arrivals"]:
        # int actual time of arrival (seconds since 1970)
        actualarrivaltime = arrival["actualarrivaltime"]
        # int actual time of departure (seconds since 1970)
        actualdeparturetime = arrival["actualdeparturetime"]
        # aircrafttype string	aircraft type ID
        aircrafttype = arrival["aircrafttype"]
        # destination string the destination ICAO airport ID
        destination = arrival["destination"]
        # destinationCity string
        destinationCity = arrival["destinationCity"]
        # destinationName string
        destinationName = arrival["destinationName"]
        # ident string flight ident or tail number
        ident = arrival["ident"]
        # origin string the origin ICAO airport ID
        origin = arrival["origin"]
        # originCity string
        originCity = arrival["originCity"]
        # originName string
        originName = arrival["originName"]

        departures.append(FlightAwareArrive(actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                                          destinationCity, destinationName, ident, origin, originCity, originName))

    return departures








def print_flightaware_departures(departures):
    for departure in departures:
        print(departure.display_flight_aware_departure_for_print())

    return


def write_flightaware_departures_to_db(departures):
    for departures in departures:
        departure.write_flightaware_arrived_to_db()

    return