# Piradar
# main.py

import dbtools

def printdict(dictionary):
	if dictionary != None:
		for header, value in dictionary.items():
			print(f"{header}: {value}")
	else:
		print(None)

# copied basic lookup interface for now - delete later
menu = input("Search for a callsign, a route, an airframe or an airport? [c/r/af/ap] ")
if menu == "c":
	print(dbtools.callsign(input("Callsign: ")))
elif menu == "r":
	print(dbtools.route(input("Route: ")))
elif menu == "af":
	printdict(dbtools.airframe(input("ICAO24 address: ")))
elif menu == "ap":
	printdict(dbtools.airport(input("IATA code: ")))
else:
	print("Invalid option")