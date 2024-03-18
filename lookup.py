# Piradar
# Lookup.py

"""
Manage and look up aircraft/airports/airlines/routes using the local database.

Functions:
    Database management
    update()
    add_routes()
    
    Lookup
    airline()
    aircraft()
    airport()
    route()
"""

import sqlite3
from csv import reader
from requests import get
from bs4 import BeautifulSoup

_DATABASE = "Main.db"
_AIRCRAFT_URL = "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv"
_AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
_AIRLINE_CODES_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"

# MARK: - Internal functions
def _get_airlines_table():
    """
    Internal, use update("airlines").
    
    Get the airlines table from wikipedia and add it to the database.
    """

    response = get(_AIRLINE_CODES_WIKI_URL, timeout=300)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="wikitable")

    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()

    try:
        cursor.execute("DROP TABLE Airlines")
    except sqlite3.OperationalError:
        pass

    cursor.execute("CREATE TABLE Airlines "
                   "('IATA code' TEXT, "
                   "'ICAO code' TEXT, "
                   "'Airline' TEXT, "
                   "'Callsign' TEXT, "
                   "'Country' TEXT)")

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]
        data += [None] * (6 - len(data))
        cursor.execute("INSERT INTO Airlines VALUES (?, ?, ?, ?, ?)", data[:5])

    cursor.close()
    main_db.commit()
    main_db.close()

def _csv_to_db(database, url, table_name, column_names):
    """
    Internal, use update() function to update a DB.

    Get a CSV from the web and add it to the database.
    Takes a database, a URL and a table name as a string and column names as a tuple.
    """

    response = get(url, timeout=300)
    data = response.text.splitlines()
    main_db = sqlite3.connect(database)
    cursor = main_db.cursor()

    try:
        cursor.execute(f"DROP TABLE {table_name}")
    except sqlite3.OperationalError:
        pass

    columns_str = ", ".join([f"'{col}' TEXT" for col in column_names])
    cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")

    csv_reader = reader(data)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute(f"INSERT INTO {table_name} "
                       f"VALUES ({', '.join(['?' for _ in range(len(column_names))])}"
                       ")", row)

    cursor.close()
    main_db.commit()
    main_db.close()

def _get_row(table, search_column, query):
    """
    Internal, use the lookup functions.
    
    Get a row from the DB as a dictionary.
    Takes a table, search column, and query as strings.
    Returns the row as a dictionary.
    """

    main_db = sqlite3.connect(_DATABASE)
    main_db.row_factory = sqlite3.Row
    cursor = main_db.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table} WHERE `{search_column}` = '{query}'")
    except sqlite3.OperationalError:
        update(table)

    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = dict(result)
    return result

# MARK: - Main functions

# MARK: Database management
def update(table):
    """
    Update a table in the database.
    Takes a table name as a string - can be "all".
    
    Updating the routes table just creates it if it doesn't exist.
    Use add_routes("/path/to/csv") to add routes.
    """

    table = table.lower()
    if table == "aircraft":
        aircraft_headers = (
            "ICAO24 address",
            "Registration",
            "Manufacturer ICAO name",
            "Manufacturer name",
            "Model",
            "Type code",
            "Serial number",
            "Line number",
            "ICAO type",
            "Operator",
            "Operator callsign",
            "Operator ICAO code",
            "Operator IATA code",
            "Owner",
            "Test registration",
            "Registered",
            "Registered until",
            "Status",
            "Built",
            "First flight",
            "Seat configuration",
            "Engines",
            "Modes",
            "ADSB",
            "ACARS",
            "Notes",
            "Category description"
        )

        _csv_to_db(_DATABASE, _AIRCRAFT_URL, "Aircraft", aircraft_headers)

    elif table == "airports":
        airport_headers = (
            "ID",
            "Identification",
            "Type",
            "Name",
            "Latitude",
            "Longitude",
            "Elevation",
            "Continent",
            "Country",
            "Reigon",
            "Municipality",
            "Scheduled service",
            "ICAO code",
            "IATA code",
            "Local code",
            "Homepage",
            "Wikipedia",
            "Keywords"
        )

        _csv_to_db(_DATABASE, _AIRPORTS_URL, "Airports", airport_headers)

    elif table == "airlines":
        _get_airlines_table()

    elif table == "routes":
        main_db = sqlite3.connect(_DATABASE)
        cursor = main_db.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'Routes'")
        if cursor.fetchone() is None:
            cursor.execute("CREATE TABLE Routes (Callsign TEXT, Origin TEXT, Destination TEXT)")

        cursor.close()
        main_db.commit()
        main_db.close()

    elif table == "all":
        for table_name in ("aircraft", "airports", "airlines", "routes"):
            update(table_name)

    else:
        print("Invalid database name")

def add_routes(csv):
    """
    Add routes to the database from CSV file.
    Takes the path to a CSV file as a string.
    """

    with open(csv, "r", newline="", encoding="utf-8") as csv_file:
        csv_reader = reader(csv_file)

        main_db = sqlite3.sqlite3.connect(_DATABASE)
        cursor = main_db.cursor()

        next(csv_reader)

        for row in csv_reader:
            cursor.execute("INSERT INTO Routes "
                           "(Callsign, "
                           "Origin, "
                           "Destination) "
                           "VALUES (?, ?, ?)", row)

        main_db.commit()
    cursor.close()
    main_db.close()

# MARK: Lookup
def airline(callsign):
    """
    Look up an aircraft.
    Takes an airline's ICAO code as a string.
    Returns airline info as a dictionary with keys as defined in _get_wiki_table().
    """

    code = callsign.upper()[:3]
    return _get_row("Airlines", "ICAO code",code)

def aircraft(address):
    """
    Look up an aircraft.
    Takes the aircraft's ICAO 24-bit address as a string.
    Returns aircraft info as a dictionary with keys as defined in update().
    """

    address = address.lower()
    return _get_row("Aircraft", "ICAO24 address",address)

def airport(iata):
    """
    Look up an airport.
    Takes the airport's 3-digit IATA code as a string.
    Returns airport info as a dictionary with keys as defined in update().
    """

    iata = iata.upper()
    return _get_row("Airports", "IATA code",iata)

def route(callsign):
    """
    Look up a route.
    Takes a callsign as a string.
    Returns the route as a dictionary with keys Callsign, Origin, and Destination.
    """

    callsign = callsign.upper()
    return _get_row("Routes", "Callsign",callsign)
