import sqlite3

database = "main.db"
airframeHeaders = ('ICAO24', 'Registration', 'Manufacturer ICAO', 'Manufacturer name', 'Model', 'Type code', 'Serial number', 'Line number', 'ICAO type', 'Operator', 'Operator callsign', 'Operator ICAO', 'Operator IATA', 'Owner', 'Test registration', 'Registered', 'Registered until', 'Status', 'Built', 'First flight', 'Seat configuration', 'Engines', 'Modes', 'ADSB', 'ACARS', 'Notes', 'Category description')

def airframe(address):
	address = address.lower()
	mainDB = sqlite3.connect(database)
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT * FROM airframes WHERE icao24 = '{address}'")
	airframeInfo = cursor.fetchone()
	cursor.close()
	mainDB.close()
	
	filteredAirframeInfo = tuple(value for value in airframeInfo if value is not None)
	pairs = zip(airframeHeaders[:len(filteredAirframeInfo)], filteredAirframeInfo)
	result = {key: value for key, value in pairs}
	return result
	
def airportICAO(iata):
	iata = iata.upper()
	mainDB = sqlite3.connect(database)
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT gps_code FROM airports WHERE iata_code = '{iata}'")
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result

def airportName(code):
	mainDB = sqlite3.connect(database)
	cursor = mainDB.cursor()
	
	if len(code) == 4:
		cursor.execute(f"SELECT name FROM airports WHERE gps_code = '{code}'")
		result = cursor.fetchone()
	elif len(code) == 3:
		cursor.execute(f"SELECT name FROM airports WHERE iata_code = '{code}'")
		result = cursor.fetchone()
	else:
		result = None
	
	result = result[0]
	return result

def airline(callsign):
	callsign = callsign.upper()
	code = callsign[:3]
	mainDB = sqlite3.connect(database)
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT Airline FROM callsigns WHERE ICAO = '{code}'")
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result

def route(callsign):
	callsign = callsign.upper()
	code = callsign[:3]
	routesTable = "routes" + code
	
	mainDB = sqlite3.connect(database)
	cursor = mainDB.cursor()
	
	cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name = '{routesTable}'")
	if (cursor.fetchone() is None):
		routesTable = "routesBAW"
	
	cursor.execute(f"SELECT Route FROM {routesTable} WHERE Callsign LIKE '%{callsign}%'")
	
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result
	
def convertDBs():
	from pandas import read_csv
	import glob
	import os
	mainDB = sqlite3.connect(database)
	
	csvs = glob.glob("*.csv")
	for database in csvs:
		db = read_csv(database)
		tableName = database.replace(".csv","")
		db.to_sql(tableName, mainDB, index=False, if_exists='replace')
		mainDB.commit()
		os.remove(database)
	
	cursor = mainDB.cursor()
	
	try:
		cursor.execute('DROP TABLE routesBAW')
		mainDB.commit()
	except:
		pass
	
	cursor.execute('''
	CREATE TABLE routesBAW AS
	SELECT "1301-1499(Domestic)" AS Callsign,  "1000-1299(Other)" AS Route
	FROM routesBAWRaw''')
	mainDB.commit()
	cursor.execute('DROP TABLE routesBAWRaw')
	mainDB.commit()
	mainDB.close()
	
def updateDBs():
	import csv
	import re
	import sys
	import requests
	from bs4 import BeautifulSoup

	response = requests.get("https://opensky-network.org/datasets/metadata/aircraftDatabase.csv")
	with open('airframes.csv', 'w', newline='', encoding='utf-8') as csvFile:
	    csvFile.write(response.text)
	
	response = requests.get("https://davidmegginson.github.io/ourairports-data/airports.csv")
	with open('airports.csv', 'w', newline='', encoding='utf-8') as csvFile:
	    csvFile.write(response.text)
	
	response = requests.get("https://en.wikipedia.org/wiki/List_of_airline_codes")
	match = re.search('<table[^>]*>(.*?)</table>', response.text, re.DOTALL)
	if match:
		tableContent = match.group(1)
	soup = BeautifulSoup(tableContent, 'html.parser')
	with open('codes.csv', 'w', newline='', encoding='utf-8') as csvFile:
		csvWriter = csv.writer(csvFile)
		rows = soup.find_all('tr')
		for row in rows:
			cells = row.find_all(['th', 'td'])
			data = [cell.get_text(strip=True) for cell in cells]
			csvWriter.writerow(data)
			
	response = requests.get("https://speedbird.online/flightnumbers.php")
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	if len(tables) >= 3:
		table = tables[2]
		rows = table.find_all('tr')
		with open('routesBAWRaw.csv', 'w', newline='', encoding='utf-8') as csvFile:
			csvWriter = csv.writer(csvFile)
			for row in rows[1:]:
				data = [cell.text.strip() for cell in row.find_all('td')]
				csvWriter.writerow(data)
	        
	convertDBs()