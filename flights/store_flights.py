import requests
import json
import sqlite3
import sys
import os
from dotenv import load_dotenv

# Amadeus credentials
AMADEUS_API_KEY = "4vvQPNk3Hj6WRHHCZy1QSqvZVgbncqA8"
AMADEUS_API_SECRET = "f2PN9OPUyXrDiIQr"
AMEDEUS_BEARER_TOKEN = ""
AMADEUS_AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"

def iataToInt(iata):
    integerKey = 0
    for char in iata[:3]:
        integerKey *= 100
        integerKey += ord(char)
    return integerKey


def get_flights(depart, arrive, date, bearer_token):
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
        'Authorization': f'Bearer {bearer_token}'
    }
    return requests.get(url, params=params, headers=headers)

def refresh_token():
    response = requests.post(
        AMADEUS_AUTH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }
    )
    return response.json()["access_token"]

def main(depart, arrive, date):

    response = get_flights(depart, arrive, date, AMEDEUS_BEARER_TOKEN)
    flights = response.json()

    if flights.get("errors", 0):
        token = refresh_token()
        response = get_flights(depart, arrive, date, token)
        flights = response.json()
    else:
        print("worked first time")

    here = os.path.dirname(__file__)
    databasePath = os.path.join(os.path.dirname(here), 'database.db')
    conn = sqlite3.connect(databasePath)
    curr = conn.cursor()
    curr.execute("""
        CREATE TABLE IF NOT EXISTS offers (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        depart_time  TEXT,
        depart_iata  TEXT,
        depart_key   INTEGER,
        arrival_time TEXT,
        arrival_iata TEXT,
        arrival_key  INTEGER,
        price_total  REAL,
        UNIQUE(depart_time, depart_iata, arrival_time, arrival_iata) ON CONFLICT IGNORE
      );""")
    conn.commit()

    for offer in flights.get('data', []):
        price = float(offer.get('price', {}).get('total', 0))
        for itinerary in offer.get('itineraries', []):
            if len(itinerary.get('segments', [])) != 1:
                continue
            seg = itinerary['segments'][0]
            departureTime = seg['departure']['at']
            departureLocation = seg['departure']['iataCode']
            arrivalTime = seg['arrival']['at']
            destination = seg['arrival']['iataCode']

            curr.execute(
              "INSERT OR IGNORE INTO offers "
              "(depart_time, depart_iata, depart_key, arrival_time, arrival_iata, arrival_key, price_total) "
              "VALUES (?, ?, ?, ?, ?, ?, ?)",
              (departureTime, departureLocation, iataToInt(departureLocation), arrivalTime, destination, iataToInt(destination), price))

    conn.commit()
    conn.close()
    print("", sep="", end="")

if __name__ == "__main__":
    try:
        depart, arrive, date = sys.argv[1:4]
    except ValueError:
        print("""Usage: python get_flights.py <DEPART LOCATION CODE> <ARRIVAL LOCATION CODE> <DEPARTURE_DATE>
        - Ex: $python store_flights.py DTW SEA 2025-05-05
        - Dates must be in the future \n""")
        sys.exit(1)
    main(depart, arrive, date)