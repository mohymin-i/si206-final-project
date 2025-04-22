import json
import sqlite3
import os

def iataToInt(iata):
    integerKey = 0
    for char in iata[:3]:
        integerKey *= 100
        integerKey += ord(char)
    return integerKey

def main():
    # load the json
    here = os.path.dirname(__file__)
    flightPath = os.path.join(here, '../utilities/output.json')
    # I had trouble running it from the main directory, this solves that issue

    with open(flightPath, 'r', encoding='utf-8') as f:
        flights = json.load(f)

    # create table
    databasePath = os.path.join(here, 'flight_offers.db')
    conn = sqlite3.connect(databasePath)
    curr = conn.cursor()
    curr.execute("""
        CREATE TABLE IF NOT EXISTS offers (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        offer_id     TEXT,
        depart_time  TEXT,
        depart_iata  TEXT,
        depart_key   INTEGER,
        arrival_time TEXT,
        arrival_iata TEXT,
        arrival_key  INTEGER,
        price_total  REAL
      );""")
    conn.commit()

    for offer in flights.get('data', []):
        offerID = offer.get('id')
        price = float(offer.get('price', {}).get('total', 0))
        # for every single iten
        for itinerary in offer.get('itineraries', []):
            # skip over non direct flights
            if len(itinerary.get('segments', [])) != 1:
                continue

            seg = itinerary['segments'][0]
            departureTime = seg['departure']['at']
            departureLocation = seg['departure']['iataCode']
            arrivalTime = seg['arrival']['at']
            destination = seg['arrival']['iataCode']

            curr.execute(
              "INSERT INTO offers "
              "(offer_id, depart_time, depart_iata, depart_key, arrival_time, arrival_iata, arrival_key, price_total) "
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (offerID, departureTime, departureLocation, iataToInt(departureLocation), arrivalTime, destination, iataToInt(destination), price))

    conn.commit()
    conn.close()
    print("Inserted offers into flight_offers.db")


if __name__ == "__main__":
    main()
