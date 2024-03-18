# Piradar
# Lookup.py

"""
Manage and look up aircraft/airports/airlines/routes using the local database
"""

import sqlite3

_DATABASE = "Main.db"
_AIRCRAFT_URL = "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv"
_AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
_CODES_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"

# MARK: Internal functions
def _get_codes_table():
    """
    Internal, use update("codes") externally
    
    Get the codes table from wikipedia and add it to the database
    """

    from requests import get
    from bs4 import BeautifulSoup

    response = get(_CODES_WIKI_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="wikitable")

    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()

    try:
        cursor.execute("DROP TABLE Codes")
    except sqlite3.OperationalError:
        pass

    cursor.execute("CREATE TABLE Codes ('IATA code' TEXT, 'ICAO code' TEXT, 'Airline' TEXT, 'Callsign' TEXT, 'Country' TEXT)")
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        data = [col.get_text(strip=True) for col in cols]
        data += [None] * (6 - len(data))
        cursor.execute("INSERT INTO Codes VALUES (?, ?, ?, ?, ?)", data[:5])

    cursor.close()
    main_db.commit()
    main_db.close()

def _csv_to_db(database, url, table_name, column_names):
    """
    Internal, use update() function to update a DB
    
    Get a CSV from the web and add it to the database
    Takes a database, a URL and a table name as a string and column names as a tuple
    """

    from requests import get
    from csv import reader

    response = get(url)
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
        cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in range(len(column_names))])})", row)

    cursor.close()
    main_db.commit()
    main_db.close()

# MARK: Main functions
def update(table):
    """
    Update a table in the database
    Takes a table name as a string (aircraft/airports/codes/routes/all)
    Updating the routes table just creates it if it doesn't exist
        Use add_routes("path/to/csv") to add routes
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

    elif table == "codes":
        _get_codes_table()

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
        for table_name in ("aircraft", "airports", "codes", "routes"):
            update(table_name)

    else:
        print("Invalid database name")

def add_routes(csv):
    """
    Add routes to the database from CSV file
    Takes the path to a CSV file as a string
    """

    from csv import reader

    with open(csv, "r", newline="", encoding="utf-8") as csv_file:
        csv_reader = reader(csv_file)

        main_db = sqlite3.sqlite3.connect(_DATABASE)
        cursor = main_db.cursor()

        next(csv_reader)

        for row in csv_reader:
            cursor.execute("INSERT INTO Routes (Callsign, Origin, Destination) VALUES (?, ?, ?)", row)

        main_db.commit()
    cursor.close()
    main_db.close()

def airline(callsign):
    """
    Look up an aircraft
    Takes an airline's ICAO code as a string
    Returns the airline's name as a string
    """

    callsign = callsign.upper()
    code = callsign[:3]
    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()
    cursor.execute(f"SELECT Airline FROM Codes WHERE `ICAO code` = '{code}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = result[0]
    return result


def aircraft(address):
    """
    Look up an aircraft
    Takes the aircraft's ICAO 24-bit address as a string
    Returns the aircraft info as a dictionary
    """

    address = address.lower()
    main_db = sqlite3.connect(_DATABASE)
    main_db.row_factory = sqlite3.Row
    cursor = main_db.cursor()
    cursor.execute(f"SELECT * FROM Aircraft WHERE `ICAO24 address` = '{address}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = dict(result)
    return result


def airport(iata):
    """
    Look up an airport
    Takes the airport's 3-digit IATA code as a string
    Returns the airport info as a dictionary
    """

    iata = iata.upper()
    main_db = sqlite3.connect(_DATABASE)
    main_db.row_factory = sqlite3.Row
    cursor = main_db.cursor()
    cursor.execute(f"SELECT * FROM Airports WHERE `IATA code` = '{iata}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = dict(result)
    return result

def route(callsign):
    """
    Look up a route
    Takes a callsign as a string
    Returns the route as a dictionary with keys Callsign, Origin, Destination
    """

    callsign = callsign.upper()
    main_db = sqlite3.connect(_DATABASE)
    main_db.row_factory = sqlite3.Row
    cursor = main_db.cursor()
    cursor.execute(f"SELECT * FROM Routes WHERE `Callsign` = '{callsign}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = dict(result)
    return result
