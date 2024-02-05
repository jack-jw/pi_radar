import lookup

details = lookup.address(input("ICAO24: "))

if details != None:
    for index in range(1,27):
        if details[index] != "":
            print(lookup.airframeHeaders[index],"-",details[index])
else:
    print("Not available")
    