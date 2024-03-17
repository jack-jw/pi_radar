# Piradar
# main.py

import lookup

def printdict(dictionary):
	if dictionary != None:
		for header, value in dictionary.items():
			print(f"{header}: {value}")
	else:
		print(None)

# copied basic lookup interface for now - delete later
menu = input("Search for a airline, a route, an airframe or an airport? [l/r/f/p] ")
if menu == "l":
	print(lookup.airline(input("Callsign: ")))
elif menu == "r":
	print(lookup.route(input("Route: ")))
elif menu == "f":
	printdict(lookup.airframe(input("ICAO24 address: ")))
elif menu == "p":
	printdict(lookup.airport(input("IATA code: ")))
else:
	print("Invalid option")
