#!/usr/bin/python3
import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

from flightawarelib import config

# FlightAwareArrived class

# https://flightaware.com/commercial/flightxml/explorer/#op_Arrived

# from FlightXML2 Explorer: Arrived returns information about flights that have recently arrived for the specified
# airport and maximum number of flights to be returned. Flights are returned from most to least recent. Only flights
# that arrived within the last 24 hours are considered.

# Times returned are seconds since 1970 (UNIX epoch seconds).


class ArrivalStruct:

    def __init__(self, actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                 destinationcity, destinationname, ident, origin, origincity, originname):
        self.actualarrivaltime = datetime.fromtimestamp(actualarrivaltime)
        self.actualdeparturetime = datetime.fromtimestamp(actualdeparturetime)
        self.aircrafttype = aircrafttype
        self.destination = destination
        self.destinationCity = destinationcity
        self.destinationName = destinationname
        self.ident = ident
        self.origin = origin
        self.originCity = origincity
        self.originName = originname


class FlightAwareArrived:

    def __init__(self):

        self.flightawareapiuser = config.FA_USER
        self.flightawareapikey = config.FA_KEY

    def display_flight_aware_arrived_for_print(self, arrival):
        output = "Flight {0} ({1})\n" + \
                 "Departing: {2}-{3}({4}) at {5}\n" + \
                 "Arriving:  {6}-{7}({8}) at {9}\n"

        return output.format(arrival.ident, arrival.aircrafttype, arrival.originName, arrival.originCity, arrival.origin,
                             arrival.actualdeparturetime, arrival.destinationName, arrival.destinationCity,
                             arrival.destination, arrival.actualarrivaltime)

    def display_flight_aware_arrived_for_csv(self):
        return ""

    def write_flightaware_arrived_to_db(self, arrival):

        # TODO Move this to using an O:RM approach

        # open database connection
        db = pymysql.connect(config.FAL_DBHOST,
                             config.FAL_DBUSER,
                             config.FAL_DBPASS,
                             config.FAL_DBNAME)

        # prepare a cursor object
        cursor = db.cursor()

        # prepare SQL statement
        statement = "INSERT INTO Arrived(ACTUAL_ARRIVAL_TIME, " + \
                    "ACTUAL_DEPARTURE_TIME, AIRCRAFT_TYPE, DESTINATION, " + \
                    "DESINTATION_CITY, DESTINATION_NAME, IDENT, ORIGIN, " + \
                    "ORIGIN_CITY, ORIGIN_NAME) VALUES (%s, %s, %s," + \
                    "%s, %s, %s, %s, %s, %s, %s)"

        data = (arrival.actualarrivaltime, arrival.actualdeparturetime, arrival.aircrafttype,
                arrival.destination, arrival.destinationCity, arrival.destinationName,
                arrival.ident, arrival.origin, arrival.originCity, arrival.originName)

        # print(statement)

        # give it a shot
        try:
            # Execute the SQL command
            cursor.execute(statement, data)
            # commit/save changes
            db.commit()
        except Exception as exp:
            # rollback changes in case of error
            print('things went bad: ' + str(exp))
            db.rollback()

        # disconnect from server
        db.close()

        return

    def get_flightaware_arrived(self, airport, filterType, howMany, offset):

        # hold arrivals objects
        arrivals = []

        user = self.flightawareapiuser
        key = self.flightawareapikey

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
            destinationcity = arrival["destinationCity"]
            # destinationName string
            destinationname = arrival["destinationName"]
            # ident string flight ident or tail number
            ident = arrival["ident"]
            # origin string the origin ICAO airport ID
            origin = arrival["origin"]
            # originCity string
            origincity = arrival["originCity"]
            # originName string
            originname = arrival["originName"]

            arrivals.append(ArrivalStruct(actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                                          destinationcity, destinationname, ident, origin, origincity,
                                          originname))

        return arrivals

    def print_flightaware_arrived(self, arrivals):
        for arrival in arrivals:
            print(self.display_flight_aware_arrived_for_print(arrival))

        return

    def write_flightaware_arrivals_to_db(self, arrivals):
        for arrival in arrivals:
            self.write_flightaware_arrived_to_db(arrival)

        return
