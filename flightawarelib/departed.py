#!/usr/bin/python3
import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

from flightawarelib import config

# FlightAwareDeparted class

# https://flightaware.com/commercial/flightxml/explorer/#op_Arrived

# Departed returns information about already departed flights for a specified airport and maximum number of flights
# to be returned. Departed flights are returned in order from most recently to least recently departed. Only flights
# that have departed within the last 24 hours are considered.
#
# Times returned are seconds since 1970 (UNIX epoch seconds).


class DepartureStruct:

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


class FlightAwareDeparted:

    def __init__(self):

        self.flightawareapiuser = config.FA_USER
        self.flightawareapikey = config.FA_KEY

    def display_flight_aware_departed_for_print(self, departure):
        output = "Flight {0} ({1})\n" + \
                 "Departing: {2}-{3}({4}) at {5}\n" + \
                 "Arriving:  {6}-{7}({8}) at {9}\n"

        return output.format(departure.ident, departure.aircrafttype, departure.originName, departure.originCity, departure.origin,
                             departure.actualdeparturetime, departure.destinationName, departure.destinationCity,
                             departure.destination, departure.actualarrivaltime)

    def display_flight_aware_departed_for_csv(self):
        return ""

    def write_flightaware_departed_to_db(self, departure):

        # TODO Move this to using an O:RM approach

        # open database connection
        db = pymysql.connect(config.FAL_DBHOST,
                             config.FAL_DBUSER,
                             config.FAL_DBPASS,
                             config.FAL_DBNAME)

        # prepare a cursor object
        cursor = db.cursor()

        # prepare SQL statement
        statement = "INSERT INTO Departed(ACTUAL_ARRIVAL_TIME, " + \
                    "ACTUAL_DEPARTURE_TIME, AIRCRAFT_TYPE, DESTINATION, " + \
                    "DESINTATION_CITY, DESTINATION_NAME, IDENT, ORIGIN, " + \
                    "ORIGIN_CITY, ORIGIN_NAME) VALUES (%s, %s, %s," + \
                    "%s, %s, %s, %s, %s, %s, %s)"

        data = (departure.actualarrivaltime, departure.actualdeparturetime, departure.aircrafttype,
                departure.destination, departure.destinationCity, departure.destinationName,
                departure.ident, departure.origin, departure.originCity, departure.originName)

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

    def get_flightaware_departed(self, airport, filtertype, howmany, offset):

        # hold arrivals objects
        departures = []

        user = self.flightawareapiuser
        key = self.flightawareapikey

        # Service URL
        url = "http://flightxml.flightaware.com/json/FlightXML2/Arrived?airport=" + airport + \
              "&filter=" + filtertype + "&howMany=" + str(howmany) + "&offset=" + str(offset)

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

            departures.append(DepartureStruct(actualarrivaltime, actualdeparturetime, aircrafttype, destination,
                                                destinationcity, destinationname, ident, origin, origincity,
                                                originname))

        return departures

    def print_flightaware_departed(self, departures):
        for departure in departures:
            print(self.display_flight_aware_departed_for_print(departure))

        return

    def write_flightaware_departures_to_db(self, departures):
        for departure in departures:
            self.write_flightaware_departed_to_db(departure)

        return
