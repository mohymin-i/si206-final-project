import requests
import json
import sqlite3
import sys
import os
from dotenv import load_dotenv


# Amedus (flights)
AMEDUS_BEARER_TOKEN="EpvQnrm8s4GYiuRHWLpAgTViMO2J"
AMEDUS_API_KEY="4vvQPNk3Hj6WRHHCZy1QSqvZVgbncqA8"
AMEDUS_API_SECRET="f2PN9OPUyXrDiIQr"

def main(depart, arrive, date):
    load_dotenv()
    url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    params = {
    "originLocationCode": depart,
    "destinationLocationCode": arrive,
    "departureDate": date,
    "adults": 1,
    "nonStop": "true",
    "max": 10,
    "currencyCode": "USD"
    }
    headers = {
    'Authorization': f'Bearer {AMEDUS_BEARER_TOKEN}' # mispelled AMADEUS lol
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    #print(data)

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
            # print("Written to file") Quieted, too much output
            print("", sep="", end="") # so we don't just spam the temrinal with whitespace
        except Exception as e:
            print("failed to write response to file:", e)


if __name__ == "__main__":
    try:
        depart, arrive, date = sys.argv[1:4]
    except ValueError:
        print("""Usage: python get_flights.py <DEPART LOCATION CODE> <ARRIVAL LOCATION CODE> <DEPARTURE_DATE>
        - Ex: $python get_flights.py DTW SEA 2025-05-05
        - Dates must be in the future \n""")
        sys.exit(1)
    main(depart, arrive, date)