# main.py

import lib

# copied basic lookup interface for now - delete later
menu = input("Search for a callsign, a route, or an airframe from an address? [c/r/a] ")
if menu == "c":
	print(lib.callsign(input("Callsign: ")))
elif menu == "r":
	print(lib.route(input("Route: ")))
elif menu == "a":
	details = lib.airframe(input("ICAO24 address: "))
	if details != None:
		for header, value in details.items():
			print(f"{header}: {value}")
	else:
		print(None)
else:
	print("Invalid option")