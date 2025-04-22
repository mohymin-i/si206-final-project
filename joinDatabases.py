import sqlite3
import os
import sys

# Usage
# Go to flights and run populate_database.py to create flights
# Go to weather and create weather database


def main():
    here = os.path.dirname(__file__)
    # paths to databases
    flights_db  = os.path.join(here, 'flights',       'flight_offers.db')
    airports_db = os.path.join(here, 'airport_codes',  'airport_codes.db')
    weather_db  = os.path.join(here, 'weather',        'weather.db')
    combined_db = os.path.join(here, 'combined.db')

    # check databses exist
    for label, path in [('Flights DB', flights_db),
                        ('Airports DB', airports_db),
                        ('Weather DB', weather_db)]:
        if not os.path.exists(path):
            print(f"Error: {label} not found at {path}")
            sys.exit(1)

    # Open (or create) the combined database
    conn = sqlite3.connect(combined_db)
    curr = conn.cursor()

    # Attach source DBs
    curr.execute("ATTACH DATABASE ? AS flights_db",  (flights_db,))
    curr.execute("ATTACH DATABASE ? AS airports_db", (airports_db,))
    curr.execute("ATTACH DATABASE ? AS weather_db",  (weather_db,))

    # combined offers
    # flights API and airport API, combines the two into a table with flight info and airport and city names
    curr.execute("DROP TABLE IF EXISTS main.combined_offers;")
    curr.execute(
        """
        CREATE TABLE main.combined_offers AS
        SELECT
          o.depart_time,
          o.depart_iata,
          ad.city        AS depart_city,
          ad.country     AS depart_country,
          ad.integer_key AS depart_key,
          o.arrival_time,
          o.arrival_iata,
          aa.city        AS arrival_city,
          aa.country     AS arrival_country,
          aa.integer_key AS arrival_key,
          o.price_total
        FROM flights_db.offers o
        LEFT JOIN airports_db.airports ad ON ad.iata_code = o.depart_iata
        LEFT JOIN airports_db.airports aa ON aa.iata_code = o.arrival_iata;
        """
    )

    # Copy the weather tables over, no need to modify or merge
    curr.execute("DROP TABLE IF EXISTS main.headline;")
    curr.execute("CREATE TABLE main.headline AS SELECT * FROM weather_db.headline;")

    curr.execute("DROP TABLE IF EXISTS main.daily;")
    curr.execute("CREATE TABLE main.daily AS SELECT * FROM weather_db.daily;")

    conn.commit()
    conn.close()

    print(f"Combined DB created at {combined_db} with tables: combined_offers, headline, daily.")

if __name__ == '__main__':
    main()
