# To Do
# Price ranges for a single trip
# Average price by travel data

import json
import subprocess
import sqlite3


# file path names, easier than changing names
flightsPath = "flights/output.json"
airportsPath = "airport_codes/output.json"
weatherPath = "weather/output.json"

# def getAirportCodes(airport_name): 
#     # 
#     airportCodes = ["INVALID"] # return this by default
#     with open(airportsPath, "r") as airports:
#         data = json.load(airports)
    
#     # get code if in name in file
#     for name in data:
#         if airport_name in name:
#             airportCodes = [] # clear the list
#             for airport in data[name]:
#                 airportCodes.append(airport[0])
#     return airportCodes

# def priceRangeHelper(code1, code2, ):
#     pass

# def getPriceRanges(startLocation, endLocation, date):
#     # assumes the user has no preference for airport
#     start_codes = getAirportCodes(startLocation)
#     end_codes = getAirportCodes(endLocation)

#     priceRanges = []
#     return priceRanges

# make a database for the flightPaths
def main():
    with open(flightsPath, "r", encoding="utf-8") as ff: flights = json.load(ff)
    with open(airportsPath, "r", encoding="utf-8") as fa: airports = json.load(fa)
    with open(airportsPath, "r", encoding="utf-8") as fw: weather = json.load(fw)

    



    return 0

if __name__ == "__main__":
    main()
    