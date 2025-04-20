# To Do
# Price ranges for a single trip
# Average price by travel data

import json
import subprocess


# file path names, easier than changing names
flightsPath = "flights/output.json"
airportsPath = "airport_codes/output.json"
weatherPath = "weather/output.json"

def getAirportCodes(airport_name):
    airportCodes = ["INVALID"] # return this by default
    with open(airportsPath, "r") as airports:
        data = json.load(airports)
    
    # get code if in name in file
    for name in data:
        if airport_name in name:
            airportCodes = [] # clear the list
            for airport in data[name]:
                airportCodes.append(airport[0])
    return airportCodes

def priceRangeHelper(code1, code2, ):
    pass

def getPriceRanges(startLocation, endLocation, date):
    # assumes the user has no preference for airport
    start_codes = getAirportCodes(startLocation)
    end_codes = getAirportCodes(endLocation)

    priceRanges = []
    return priceRanges

def main():
    print(getAirportCodes("Aberdeen"))

if __name__ == "__main__":
    main()
    