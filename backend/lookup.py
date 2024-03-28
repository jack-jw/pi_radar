# Piradar
# lookup.py

"""
Manage and look up aircraft/airports/airlines/routes using the local databases.

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
import requests
from bs4 import BeautifulSoup

_DATABASE = "./instance/local.db"
_INSTANCE_DATABASE = "./instance/instance.db"
_AIRCRAFT_URL = "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv"
_AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
_AIRLINE_CODES_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"

# MARK: - Internal functions
def _get_airlines_table():
    """
    Internal, use update("airlines").
    
    Get the airlines table from wikipedia and add it to the database.
    """

    try:
        response = requests.get(_AIRLINE_CODES_WIKI_URL, timeout=120)
        if not response.ok:
            return
    except requests.exceptions.ReadTimeout:
        return

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="wikitable")

    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()

    try:
        cursor.execute("DROP TABLE airlines")
    except sqlite3.OperationalError:
        pass

    cursor.execute("CREATE TABLE airlines "
                   "('iata' TEXT, "
                   "'icao' TEXT, "
                   "'name' TEXT, "
                   "'radio' TEXT, "
                   "'country' TEXT)")

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]
        data += [None] * (6 - len(data))
        cursor.execute("INSERT INTO airlines VALUES (?, ?, ?, ?, ?)", data[:5])

    cursor.close()
    main_db.commit()
    main_db.close()

def _csv_to_db(database, url, table_name, column_names):
    """
    Internal, use update() function to update a DB

    Get a CSV from the web and add it to the database
    Takes a database, a URL and a table name as a string and column names as a tuple
    """

    try:
        response = requests.get(url, timeout=300)
        if not response.ok:
            return
    except requests.exceptions.ReadTimeout:
        return

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

    db_path = _INSTANCE_DATABASE if table == "routes" else _DATABASE
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    while True:
        try:
            cursor.execute(f"SELECT * FROM {table} WHERE `{search_column}` = '{query}'")
            break
        except sqlite3.OperationalError:
            update(table)

    result = cursor.fetchone()
    cursor.close()
    db.close()

    if result:
        result = dict(result)
        for key, value in result.copy().items():
            if not value:
                del result[key]
    else:
        result = {}
        result[search_column] = query

    return result

# MARK: - Main functions

# MARK: Database management
def check():
    """
    Checks the tables/DBs are there
    If they aren't, create and update them
    """
    
    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()
    for table in ("airlines","aircraft","airports"):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if cursor.fetchone() is None:
            update(table)
    cursor.close()
    main_db.close()
    update("routes")

def update(table):
    """
    Update a table in the database.
    Takes a table name as a string.
    
    Updating the routes table just creates it if it doesn't exist.
    Use add_routes("/path/to/csv") to add routes.
    """

    table = table.lower()
    if table == "aircraft":
        aircraft_headers = (
            "icao24",
            "reg",
            "manicao",
            "man",
            "model",
            "type",
            "serial",
            "linenum",
            "typecode",
            "operator",
            "operatorcallsign",
            "operatoricao",
            "operatoriata",
            "owner",
            "testreg",
            "reged",
            "regeduntil",
            "status",
            "built",
            "firstflight",
            "seatconfig",
            "engines",
            "modes",
            "adsb",
            "acars",
            "notes",
            "categorydesc"
        )

        _csv_to_db(_DATABASE, _AIRCRAFT_URL, "aircraft", aircraft_headers)

    elif table == "airports":
        airport_headers = (
            "id",
            "ident",
            "type",
            "name",
            "lat",
            "lng",
            "elevation",
            "continent",
            "country",
            "region",
            "muni",
            "airlines",
            "icao",
            "iata",
            "local",
            "website",
            "wiki",
            "keywords"
        )

        _csv_to_db(_DATABASE, _AIRPORTS_URL, "airports", airport_headers)

    elif table == "airlines":
        _get_airlines_table()

    elif table == "routes":
        instance_db = sqlite3.connect(_INSTANCE_DATABASE)
        cursor = instance_db.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'routes'")
        if cursor.fetchone() is None:
            cursor.execute("CREATE TABLE routes ('callsign' TEXT, 'origin' TEXT, 'destination' TEXT)")

        cursor.close()
        instance_db.commit()
        instance_db.close()

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

        instance_db = sqlite3.connect(_INSTANCE_DATABASE)
        cursor = instance_db.cursor()

        next(csv_reader)

        for row in csv_reader:
            cursor.execute("INSERT INTO routes ("
                           "callsign, "
                           "origin, "
                           "destination"
                           ") VALUES (?, ?, ?)", row)

        instance_db.commit()
    cursor.close()
    instance_db.close()

def add_origin(callsign, origin):

    if not (callsign and origin):
        return

    instance_db = sqlite3.connect(_INSTANCE_DATABASE)
    cursor = instance_db.cursor()
    cursor.execute("SELECT * FROM routes WHERE callsign = ?", (callsign,))
    row_exists = cursor.fetchone()
    
    if row_exists:
        cursor.execute("UPDATE routes SET origin = ? WHERE callsign = ?", (origin, callsign))
    else:
        cursor.execute("INSERT INTO Routes ("
                       "callsign, "
                       "origin, "
                       "destination"
                       ") VALUES (?, ?, NULL)", (callsign, origin))
    
    instance_db.commit()
    cursor.close()
    instance_db.close()

def add_destination(callsign, destination):

    if not (callsign and destination):
        return

    instance_db = sqlite3.connect(_INSTANCE_DATABASE)
    cursor = instance_db.cursor()
    cursor.execute("SELECT * FROM routes WHERE callsign = ?", (callsign,))
    row_exists = cursor.fetchone()
    
    if row_exists:
        cursor.execute("UPDATE routes SET destination = ? WHERE callsign = ?", (destination, callsign))
    else:
        cursor.execute("INSERT INTO Routes ("
                       "callsign, "
                       "origin, "
                       "destination"
                       ") VALUES (?, NULL, ?)", (callsign, destination))
    
    instance_db.commit()
    cursor.close()
    instance_db.close()

# MARK: Lookup
def airline(callsign):
    """
    Look up an aircraft
    Takes an airline's ICAO code as a string
    - will automatically slice a callsign
    Returns airline info as a dictionary with keys as defined in _get_airlines_table()
    """

    if not callsign:
        return None

    if not any(char.isdigit() for char in callsign):
        return None

    code = callsign.upper()[:3]
    result = _get_row("airlines", "icao",code)
    if result:
        return result
    else:
        return {"icao": code}

def aircraft(address):
    """
    Look up an aircraft.
    Takes the aircraft's ICAO 24-bit address as a string.
    Returns aircraft info as a dictionary with keys as defined in update().
    """

    if not address:
        return

    address = address.lower()
    result = _get_row("aircraft", "icao24",address)
    if result:
        return result
    else:
        return {"icao24": address}

def airport(code):
    """
    Look up an airport.
    Takes the airport's IATA or ICAO code as a string.
    Returns airport info as a dictionary with keys as defined in update().
    """
    
    if not code:
        return

    code = code.upper()
    if len(code) == 3:
        code = code.upper()
        return _get_row("airports", "iata",code)
    elif len(code) == 4:
        code = code.upper()
        return _get_row("airports", "icao",code)

def route(callsign):
    """
    Look up a route.
    Takes a callsign as a string.
    Returns the route as a dictionary with keys Callsign, Origin, and Destination.
    """

    callsign = callsign.upper()
    result = _get_row("routes", "callsign",callsign)
    return result
