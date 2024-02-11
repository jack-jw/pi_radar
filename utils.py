import sqlite3

airframeHeaders = ('ICAO24', 'Registration', 'Manufacturer ICAO', 'Manufacturer name', 'Model', 'Type code', 'Serial number', 'Line number', 'ICAO type', 'Operator', 'Operator callsign', 'Operator ICAO', 'Operator IATA', 'Owner', 'Test registration', 'Registered', 'Registered until', 'Status', 'Built', 'First flight', 'Seat configuration', 'Engines', 'Modes', 'ADSB', 'ACARS', 'Notes', 'Category description')

def airframe(address):
	address = address.lower()
	mainDB = sqlite3.connect('main.db')
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
	mainDB = sqlite3.connect('main.db')
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT gps_code FROM airports WHERE iata_code = '{iata}'")
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result

def airportName(code):
	mainDB = sqlite3.connect('main.db')
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

def callsign(callsign):
	callsign = callsign.upper()
	callsign = callsign[:3]
	mainDB = sqlite3.connect('main.db')
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT Airline FROM callsigns WHERE ICAO = '{callsign}'")
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result

def route(route):
	route = route.upper()
	callsign = route[:3]
	routesTable = "routes" + callsign
	mainDB = sqlite3.connect('main.db')
	cursor = mainDB.cursor()
	cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name = '{routesTable}'")
	if (cursor.fetchone() is not None) and callsign != "BAW":
		print("\nA\n")
		cursor.execute(f"SELECT Route FROM " + routesTable + " WHERE Callsign = '{route}'")
	else:
		cursor.execute(f"SELECT `1000-1299(Other)` FROM routesBAW WHERE `1301-1499(Domestic)` LIKE '%{route}%'")
	result = cursor.fetchone()
	cursor.close()
	mainDB.close()
	result = result[0]
	return result
	
def convertDBs():
	from pandas import read_csv
	import glob
	import os
	mainDB = sqlite3.connect("main.db")
	
	csvs = glob.glob("*.csv")
	for database in csvs:
		db = read_csv(database)
		tableName = database.replace(".csv","")
		db.to_sql(tableName, mainDB, index=False, if_exists='replace')
		os.remove(database)
	
	mainDB.commit()
	mainDB.close()
	
def fetchDBs():
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
	
	response = requests.get("https://speedbird.online/flightnumbers.php")
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	if len(tables) >= 3:
		table = tables[2]
		rows = table.find_all('tr')
		with open('routesBAW.csv', 'w', newline='', encoding='utf-8') as csvFile:
			csvWriter = csv.writer(csvFile)
			for row in rows[1:]:
				data = [cell.text.strip() for cell in row.find_all('td')]
				csvWriter.writerow(data)
	
	response = requests.get("https://en.wikipedia.org/wiki/List_of_airline_codes")
	match = re.search('<table[^>]*>(.*?)</table>', response.text, re.DOTALL)
	if match:
		tableContent = match.group(1)
	soup = BeautifulSoup(tableContent, 'html.parser')
	with open('callsigns.csv', 'w', newline='', encoding='utf-8') as csvFile:
		csvWriter = csv.writer(csvFile)
		rows = soup.find_all('tr')
		for row in rows:
			cells = row.find_all(['th', 'td'])
			data = [cell.get_text(strip=True) for cell in cells]
			csvWriter.writerow(data)
	        
	convertDBs()