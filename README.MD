# FlightAware Lib

A Python 3 Wrapper for the FlightAware XML 2 API

## DotEnv

It is necessary to create a __.env__ file to configure the following ENVIRONMENT variables:

* FAL_DBHOST  => your database host (MySQL)
* FAL_DBUSER  => database user (MySQL)
* FAL_DBPASS  => database password
* FAL_DBTABLE => database table 
* FA_USER => FlightAware user account
* FA_KEY  => FlightAware XML 2.0 Key

for example you would place information like this in the `.env` file:

```
FAL_DBHOST  = 123.123.123.123
FAL_DBUSER  = flightdatauser
FAL_DBPASS  = password
FAL_DBNAME = flightdata
FA_USER = flightdatauser
FA_KEY  = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### To Do

* Configure database schema for entire library
* Implement remaining FlightAware XML 2.0 objects

### Change Log

Version 0.0.1

* only Arrived responses write to the database - experimental feature, don't use yet 