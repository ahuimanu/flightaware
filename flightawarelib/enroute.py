#!/usr/bin/python3
import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

from flightawarelib import config

# FlightAwareEnroute class

# https://flightaware.com/commercial/flightxml/explorer/#op_Enroute

# Enroute returns information about flights already in the air heading towards the specified airport and also flights
# scheduled to arrive at the specified airport. Enroute flights are returned from soonest estimated arrival to least
# soon estimated arrival. The howMany argument specifies the maximum number of flights to be returned.
#
# Times returned are seconds since 1970 (UNIX epoch seconds).


class EnrouteStruct:

    def __init__(self, actualdeparturetime, aircrafttype, destination, destinationcity, destinationname,
                 estimatedarrivaltime, fileddeparturetime, ident, origin, origincity, originname):
        self.actualdeparturetime = datetime.fromtimestamp(actualdeparturetime)
        self.aircrafttype = aircrafttype
        self.destination = destination
        self.destinationcity = destinationcity
        self.destinationname = destinationname
        self.estimatedarrivaltime = datetime.fromtimestamp(estimatedarrivaltime)
        self.fileddeparturetime = datetime.fromtimestamp(fileddeparturetime)
        self.ident = ident
        self.origin = origin
        self.origincity = origincity
        self.originname = originname


class FlightAwareEnroute:

    def __init__(self):

        self.flightawareapiuser = config.FA_USER
        self.flightawareapikey = config.FA_KEY

    def display_flight_aware_enroute_for_print(self, enroute):
        output = "Flight {0} ({1})\n" + \
                 "Departing: {2}-{3}({4}) at {5}\n" + \
                 "Arriving:  {6}-{7}({8}) at {9}\n"

        return output.format(enroute.ident, enroute.aircrafttype,
                             enroute.originname, enroute.origincity, enroute.origin, enroute.actualdeparturetime,
                             enroute.destinationname, enroute.destinationcity, enroute.destination,
                             enroute.estimatedarrivaltime)

    def display_flight_aware_enroute_for_csv(self):
        return ""

    def write_flightaware_enroute_to_db(self, enroute):

        # TODO Move this to using an O:RM approach

        # open database connection
        db = pymysql.connect(config.FAL_DBHOST,
                             config.FAL_DBUSER,
                             config.FAL_DBPASS,
                             config.FAL_DBNAME)

        # prepare a cursor object
        cursor = db.cursor()

        # prepare SQL statement
        statement = "INSERT INTO Enroute( ACTUAL_DEPARTURE_TIME, AIRCRAFT_TYPE, DESTINATION, DESINTATION_CITY, " + \
                    "DESTINATION_NAME, ESTIMATED_ARRIVAL_TIME, FILED_DEPARTURE_TIME, IDENT, ORIGIN, ORIGIN_CITY, " + \
                    "ORIGIN_NAME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        data = (enroute.actualdeparturetime, enroute.aircrafttype, enroute.destination, enroute.destinationcity,
                enroute.destinationname, enroute.estimatedarrivaltime, enroute.fileddeparturetime,
                enroute.ident, enroute.origin, enroute.origincity, enroute.originname)

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

    def get_flightaware_enroute(self, airport, filtertype, howmany, offset):

        # hold arrivals objects
        enroutes = []

        user = self.flightawareapiuser
        key = self.flightawareapikey

        # Service URL
        url = "http://flightxml.flightaware.com/json/FlightXML2/Enroute?airport=" + airport + \
              "&filter=" + filtertype + "&howMany=" + str(howmany) + "&offset=" + str(offset)

        # make request
        req = requests.get(url, auth=(user, key))

        # translate to JSON
        flightaware = req.json()

        # TODO place the keys below into variables

        for enroute in flightaware["EnrouteResult"]["enroute"]:
            # int actual time of departure (seconds since 1970)
            actualdeparturetime = enroute["actualdeparturetime"]
            # aircrafttype string	aircraft type ID
            aircrafttype = enroute["aircrafttype"]
            # destination string the destination ICAO airport ID
            destination = enroute["destination"]
            # destinationCity string
            destinationcity = enroute["destinationCity"]
            # destinationName string
            destinationname = enroute["destinationName"]
            # int estimated time of arrival (seconds since 1970)
            estimatedarrivaltime = enroute["estimatedarrivaltime"]
            # int filed time of departure (seconds since 1970)
            fileddeparturetime = enroute["filed_departuretime"]
            # ident string flight ident or tail number
            ident = enroute["ident"]
            # origin string the origin ICAO airport ID
            origin = enroute["origin"]
            # originCity string
            origincity = enroute["originCity"]
            # originName string
            originname = enroute["originName"]

            # the data is often not populated
            if actualdeparturetime == 0:
                actualdeparturetime = fileddeparturetime

            enroutes.append(EnrouteStruct(actualdeparturetime,
                                          aircrafttype.strip(),
                                          destination.strip(),
                                          destinationcity.strip(),
                                          destinationname.strip(),
                                          estimatedarrivaltime,
                                          fileddeparturetime,
                                          ident.strip(),
                                          origin.strip(),
                                          origincity.strip(),
                                          originname.strip()))

        return enroutes

    def print_flightaware_enroute(self, enroutes):
        for enroute in enroutes:
            print(self.display_flight_aware_enroute_for_print(enroute))

        return

    def write_flightaware_enroutes_to_db(self, enroutes):
        for enroute in enroutes:
            self.write_flightaware_enroute_to_db(enroute)

        return
