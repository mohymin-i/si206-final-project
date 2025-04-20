import requests
import json
import sqlite3
import sys
import os
from dotenv import load_dotenv

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
    'Authorization': f'Bearer {os.getenv("AMEDUS_BEARER_TOKEN")}'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    #print(data)

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
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