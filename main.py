# main.py

import lookup

# copied basic lookup interface for now - delete later
menu = input("Search for a callsign, a route, or an airframe from an address? [c/r/a] ")
if menu == "c":
	print(callsign(input("Callsign: ")))
elif menu == "r":
	print(route(input("Route: ")))
elif menu == "a":
	details = address(input("ICAO24 address: "))
	if details != None:
		for header, value in details.items():
			print(f"{header}: {value}")
	else:
		print(details)
else:
	print("Invalid option")