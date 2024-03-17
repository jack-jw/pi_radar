# Piradar
# Lookup.py

"""
Look up aircraft/airports/airlines/routes using the local database
Manage the local database
"""

import sqlite3

_DATABASE = "Main.db"

def _link(headers, dataset):
    """
    Link an array with its headers outputting a dictionary
    Maintains header orders
    """

    result = {}
    headers_range = range(len(headers) - 1)
    for row in headers_range:
        if dataset[row] is not None:
            result[headers[row]] = dataset[row]
    return result

def aircraft(address):
    """
    Look up an aircraft
    """

    address = address.lower()
    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()
    cursor.execute(f"SELECT * FROM Aircraft WHERE `ICAO24 address` = '{address}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

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

    if result:
        result = _link(aircraft_headers, result)
    return result

def airport(iata):
    """
    Look up an airport
    """

    iata = iata.upper()
    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()
    cursor.execute(f"SELECT * FROM Airports WHERE `IATA code` = '{iata}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

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

    if result:
        result = _link(airport_headers, result)
    return result

def airline(callsign):
    """
    Look up an airline
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

def route(callsign):
    """
    Look up a route
    """

    callsign = callsign.upper()
    main_db = sqlite3.connect(_DATABASE)
    cursor = main_db.cursor()
    cursor.execute(f"SELECT Route FROM Routes WHERE Callsign = '{callsign}'")
    result = cursor.fetchone()
    cursor.close()
    main_db.close()

    if result:
        result = result[0]
    return result

def _get_codes_table():
    """
    Internal, use update("codes") instead
    Get the codes table from wikipedia and add it to the database
    """

    from requests import get
    from bs4 import BeautifulSoup

    response = get("https://en.wikipedia.org/wiki/List_of_airline_codes")
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

def add_routes(csv):
    """
    Add routes to the database from CSV file
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

def _csv_to_db(database, url, table_name, column_names):
    """
    Internal, use update() function to update a DB
    Get a CSV from the web and add it to the database
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

def update(table):
    """
    Update a table in the database
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

        _csv_to_db(_DATABASE, "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv", "Aircraft", aircraft_headers)

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

        _csv_to_db(_DATABASE, "https://davidmegginson.github.io/ourairports-data/airports.csv", "Airports", airport_headers)

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
