# Piradar
# Main.py

"""
Basic lookup interface for now - delete later
"""

import lookup

def printdict(dictionary):
    """
    Prints the passed dictionary nicely.
    """

    if dictionary is not None:
        for header, value in dictionary.items():
            print(f"{header}: {value}")
    else:
        print(None)

menu = input("Search for a airline, a route, an aircraft or an airport? [l/r/c/p] ")
if menu == "l":
    print(lookup.airline(input("Callsign: ")))
elif menu == "r":
    print(lookup.route(input("Route: ")))
elif menu == "c":
    printdict(lookup.aircraft(input("ICAO24 address: ")))
elif menu == "p":
    printdict(lookup.airport(input("IATA code: ")))
else:
    print("Invalid option")
