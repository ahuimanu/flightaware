#!/usr/bin/python3
import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime

from flightawarelib import config

# Given an airport, return the METAR weather info as parsed, human-readable, and raw formats.
# If no reports are available at the requested airport but are for a nearby airport, then the reports from that airport
# may be returned instead. If a value greater than 1 is specified for howMany then multiple past reports will be
# returned, in order of increasing age. Historical data is generally only available for the last 7 days.

# Use the Metar function for a simpler interface to access just the most recent raw report.


class Metar:

    def __init__(self):

        self.flightawareapiuser = config.FA_USER
        self.flightawareapikey = config.FA_KEY

    # obtains metar data - connects to json
    def get_flightaware_metar(self, airport):

        # service URL
        url = "http://flightxml.flightaware.com/json/FlightXML2/Metar?airport={0}"
        url = url.format(airport)

        # make request to flight aware
        req = requests.get(url, auth=(self.flightawareapiuser, self.flightawareapikey))

        # returns a MetarStruct() from flight aware - will need to be converated to JSON
        # translate flightaware response to JSON

        jsonresult = req.json()

        return jsonresult["MetarResult"]


class MetarEx:

    def __init__(self):

        self.flightawareapiuser = config.FA_USER
        self.flightawareapikey = config.FA_KEY

    # obtains metar data - connects to json
    def get_flightaware_metarex_json(self, airport, starttime, howmany="10", offset="0"):

        # service URL
        url = "http://flightxml.flightaware.com/json/FlightXML2/MetarEx?airport={0}" \
              "&startTime={1}&howMany={2}&offset={3}".format(airport,
                                                             starttime,
                                                             howmany,
                                                             offset)

        # make request to flight aware
        req = requests.get(url, auth=(self.flightawareapiuser, self.flightawareapikey))

        # returns a MetarStruct() from flight aware - will need to be converated to JSON
        # translate flightaware response to JSON
        return req.json()

    def print_flightaware_metarex_from_json(self, fametarjson):

        # parse elements
        airport = fametarjson["MetarExResult"]["metar"][0]["airport"]
        cloud_altitude = fametarjson["MetarExResult"]["metar"][0]["cloud_altitude"]
        cloud_friendly = fametarjson["MetarExResult"]["metar"][0]["cloud_friendly"]
        cloud_type = fametarjson["MetarExResult"]["metar"][0]["cloud_type"]
        dewpoint = fametarjson["MetarExResult"]["metar"][0]["temp_dewpoint"]
        pressure = fametarjson["MetarExResult"]["metar"][0]["pressure"]
        raw_data = fametarjson["MetarExResult"]["metar"][0]["raw_data"]
        temperature = fametarjson["MetarExResult"]["metar"][0]["temp_air"]
        time = fametarjson["MetarExResult"]["metar"][0]["time"]
        wind_direction = fametarjson["MetarExResult"]["metar"][0]["wind_direction"]
        wind_speed = fametarjson["MetarExResult"]["metar"][0]["wind_speed"]
        wind_friendly = fametarjson["MetarExResult"]["metar"][0]["wind_friendly"]
        visibility = fametarjson["MetarExResult"]["metar"][0]["visibility"]

        output = "Airport: {0} at {1}\n" + \
                 "Temperature: {2} \u00B0C ({3} \u00B0F)\n" + \
                 "Dewpoint: {4} \u00B0C ({5} \u00B0F))\n" + \
                 "Pressure: {6}\n" + \
                 "{7} from {8} degrees at {9} knots\n" + \
                 "{10} ({11} at {12})\n" + \
                 "Visibility is {13} statute miles\n" + \
                 "Raw: {14}\n"
        output = output.format(airport,
                               datetime.fromtimestamp(time),
                               temperature,
                               self.convert_from_c_to_f(temperature),
                               dewpoint,
                               self.convert_from_c_to_f(dewpoint),
                               pressure,
                               wind_friendly,
                               wind_direction,
                               wind_speed,
                               cloud_friendly,
                               cloud_type,
                               cloud_altitude,
                               visibility,
                               raw_data)

        return output

    def convert_from_c_to_f(self, celsius):

        return celsius * 9.0/5.0 + 32
