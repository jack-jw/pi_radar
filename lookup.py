from sqlite3 import connect

_database = 'main.db'

def _link(headers, dataset):
	result = {}
	headers_range = range(len(headers) - 1)
	for row in headers_range:
		if dataset[row] is not None:
			result[headers[row]] = dataset[row]
	return result

def aircraft(address):
	address = address.lower()
	main_DB = connect(_database)
	cursor = main_DB.cursor()
	cursor.execute(f"SELECT * FROM Aircraft WHERE `ICAO24 address` = '{address}'")
	aircraft_info = cursor.fetchone()
	cursor.close()
	main_DB.close()

	aircraft_headers = ('ICAO24 address', 'Registration', 'Manufacturer ICAO name', 'Manufacturer name', 'Model', 'Type code', 'Serial number', 'Line number', 'ICAO type', 'Operator', 'Operator callsign', 'Operator ICAO code', 'Operator IATA code', 'Owner', 'Test registration', 'Registered', 'Registered until', 'Status', 'Built', 'First flight', 'Seat configuration', 'Engines', 'Modes', 'ADSB', 'ACARS', 'Notes', 'Category description')

	result = _link(aircraft_headers, aircraft_info)

	return result

def airport(iata):
	iata = iata.upper()
	main_DB = connect(_database)
	cursor = main_DB.cursor()
	cursor.execute(f"SELECT * FROM Airports WHERE `IATA code` = '{iata}'")
	airport_info = cursor.fetchone()
	cursor.close()
	main_DB.close()

	airport_headers = ('ID', 'Identification', 'Type', 'Name', 'Latitude', 'Longitude', 'Elevation', 'Continent', 'Country', 'Reigon', 'Municipality', 'Scheduled service', 'ICAO code', 'IATA code', 'Local code', 'Homepage', 'Wikipedia', 'Keywords')

	result = _link(airport_headers, airport_info)

	return result

def airline(callsign):
	callsign = callsign.upper()
	code = callsign[:3]
	main_DB = connect(_database)
	cursor = main_DB.cursor()
	cursor.execute(f"SELECT Airline FROM Codes WHERE `ICAO code` = '{code}'")
	result = cursor.fetchone()
	cursor.close()
	main_DB.close()
	result = result[0]
	return result

def route(callsign):
    callsign = callsign.upper()
    code = callsign[:3]

    main_DB = connect(_database)
    cursor = main_DB.cursor()

    cursor.execute(f"SELECT Route FROM Routes WHERE Callsign = '{callsign}'")

    result = cursor.fetchone()
    cursor.close()
    main_DB.close()
    if result:
        result = result[0]
        return result
    else:
        return None

def _get_codes_table():
	from requests import get
	from bs4 import BeautifulSoup

	response = get("https://en.wikipedia.org/wiki/List_of_airline_codes")
	soup = BeautifulSoup(response.content, "html.parser")
	table = soup.find("table", class_="wikitable")
	main_DB = connect(_database)
	cursor = main_DB.cursor()

	try:
		cursor.execute('DROP TABLE Codes')
	except:
		pass

	cursor.execute("CREATE TABLE Codes ('IATA code' TEXT, 'ICAO code' TEXT, 'Airline' TEXT, 'Callsign' TEXT, 'Country' TEXT)")
	rows = table.find_all("tr")[1:]
	for row in rows:
		cols = row.find_all("td")
		data = [col.get_text(strip=True) for col in cols]
		data += [None] * (6 - len(data))
		iata, icao, airline, callsign, country, comments = data
		cursor.execute("INSERT INTO Codes VALUES (?, ?, ?, ?, ?)", (iata, icao, airline, callsign, country))

	cursor.close()
	main_DB.commit()
	main_DB.close()

def add_routes(csv):
	from csv import reader
	
	with open(csv, "w", newline='', encoding='utf-8') as csv_file:
		csv_reader = reader(csv_file.read())
	
	next(csv_reader)
	for row in csv_reader:
		cursor.execute(f"INSERT INTO Routes VALUES ({', '.join(['?' for _ in range(len(column_names))])})", row)

	cursor.close()
	main_DB.commit()
	main_DB.close()

def _csv_to_sql(database, url, table_name, column_names):
	from requests import get
	from csv import reader

	response = get(url)
	data = response.text.splitlines()
	main_DB = connect(database)
	cursor = main_DB.cursor()

	try:
		cursor.execute(f'DROP TABLE {table_name}')
	except:
		pass

	columns_str = ', '.join([f"'{col}' TEXT" for col in column_names])
	cursor.execute(f"CREATE TABLE {table_name} ({columns_str})")
	
	csv_reader = reader(data)
	next(csv_reader)
	for row in csv_reader:
		cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in range(len(column_names))])})", row)

	cursor.close()
	main_DB.commit()
	main_DB.close()

def update(table):
    table = table.lower()
    if table == "aircraft":
        aircraft_headers = ('ICAO24 address', 'Registration', 'Manufacturer ICAO name', 'Manufacturer name', 'Model', 'Type code', 'Serial number', 'Line number', 'ICAO type', 'Operator', 'Operator callsign', 'Operator ICAO code', 'Operator IATA code', 'Owner', 'Test registration', 'Registered', 'Registered until', 'Status', 'Built', 'First flight', 'Seat configuration', 'Engines', 'Modes', 'ADSB', 'ACARS', 'Notes', 'Category description')

        _csv_to_sql(_database, "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv", "Aircraft", aircraft_headers)

    elif table == "airports":
        airports_headers = ('ID', 'Identification', 'Type', 'Name', 'Latitude', 'Longitude', 'Elevation', 'Continent', 'Country', 'Reigon', 'Municipality', 'Scheduled service', 'ICAO code', 'IATA code', 'Local code', 'Homepage', 'Wikipedia', 'Keywords')

        _csv_to_sql(_database, "https://davidmegginson.github.io/ourairports-data/airports.csv", "Airports", airports_headers)

    elif table == "codes":
        _get_codes_table()

    elif table == "routes":
        main_DB = connect(_database)
        cursor = main_DB.cursor()
        
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name = 'Routes'")
        if cursor.fetchone() is None:
            cursor.execute("CREATE TABLE Routes (Callsign TEXT, Origin TEXT, Destination TEXT)")
            
        cursor.close()
        main_DB.commit()
        main_DB.close()

    elif table == "all":
        for table_name in ("aircraft", "airports", "codes", "routes"):
            update(table_name)

    else:
        print("Invalid database name")
