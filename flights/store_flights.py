import json
import sqlite3
import os


def main():
    # load the json
    here = os.path.dirname(__file__)
    flightPath = os.path.join(here, 'output.json')
    # I had trouble running it from the main directory, this solves that issue

    with open(flightPath, 'r', encoding='utf-8') as f:
        flights = json.load(f)

    # create table
    databasePath = os.path.join(here, 'flight_offers.db')
    conn = sqlite3.connect(databasePath)
    curr = conn.cursor()
    curr.execute("""
        CREATE TABLE IF NOT EXISTS offers (
        offer_id     TEXT,
        depart_time  TEXT,
        depart_iata  TEXT,
        arrival_time TEXT,
        arrival_iata TEXT,
        price_total  REAL,
        PRIMARY KEY(offer_id, depart_time)
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
              "INSERT OR REPLACE INTO offers "
              "(offer_id, depart_time, depart_iata, arrival_time, arrival_iata, price_total) "
              "VALUES (?, ?, ?, ?, ?, ?)",
              (offerID, departureTime, departureLocation, arrivalTime, destination, price))

    conn.commit()
    conn.close()
    print("Inserted offers into flight_offers.db")


if __name__ == "__main__":
    main()