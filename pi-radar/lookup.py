# lookup

import csv
import os

# ICAO24 lookup function
def address(address):
    address = address.lower()
    with open("airframes.csv", 'r') as rawDatabase: # open database
        database = csv.reader(rawDatabase) # convert CSVs to 2D list
        for row in database: # linear search
            if address in row[0]: # row[0] is ICAO24 address
                return row # return the row if the address matches

# Callsign lookup function
def callsign(callsign):
    callsign = callsign.upper()
    callsign = callsign[:3]
    
    with open("callsigns.csv", 'r') as rawDatabase: # open database
        database = csv.reader(rawDatabase) # convert CSVs to 2D list
        for row in database: # linear search
            if callsign in row[0]: # row[0] is ICAO callsign
                return row[1]

# Route lookup function
def route(route):
    route = route.upper()
    callsign = route[:3]
    routesDatabase = "routes" + callsign + ".csv"
    
    if os.path.exists(routesDatabase) == False: # fallback on routesBAW.csv
        routesDatabase = "routesBAW.csv"
    
    with open(routesDatabase, 'r') as rawDatabase: # open database
        database = csv.reader(rawDatabase) # convert CSVs to 2D list
        
        if routesDatabase != "routesBAW.csv":
            for row in database:
                if route in row[0]:
                    return row[1]
        else:
            for row in database: # linear search
                for item in row:
                    if route in item:
                        return row[3]

# Define headers
airframeHeaders = ['ICAO24', 'Registration', 'Manufacturer ICAO', 'Manufacturer name', 'Model', 'Type code', 'Serial number', 'Line number', 'ICAO type', 'Operator', 'Operator callsign', 'Operator ICAO', 'Operator IATA', 'Owner', 'Test registration', 'Registered', 'Registered until', 'Status', 'Built', 'First flight', 'Seat configuration', 'Engines', 'Modes', 'ADSB', 'ACARS', 'Notes', 'Category description']