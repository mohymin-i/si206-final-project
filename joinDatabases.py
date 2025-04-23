import sqlite3
import os
import sys

def main():
    here = os.path.dirname(__file__)
    # paths to databases
    flights_db  = os.path.join(here, 'flights',       'flight_offers.db')
    airports_db = os.path.join(here, 'airport_codes',  'airport_codes.db')
    weather_db  = os.path.join(here, 'weather',        'weather.db')
    combined_db = os.path.join(here, 'combined.db')

    # check databases exist…
    for label, path in [('Flights DB', flights_db),
                        ('Airports DB', airports_db),
                        ('Weather DB', weather_db)]:
        if not os.path.exists(path):
            print(f"Error: {label} not found at {path}")
            sys.exit(1)

    conn = sqlite3.connect(combined_db)
    curr = conn.cursor()

    curr.execute("ATTACH DATABASE ? AS flights_db",  (flights_db,))
    curr.execute("ATTACH DATABASE ? AS airports_db", (airports_db,))
    curr.execute("ATTACH DATABASE ? AS weather_db",  (weather_db,))


    # create new combined offers
    curr.execute("""
        CREATE TABLE IF NOT EXISTS main.combined_offers (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,  -- NEW: auto‑incrementing ID
            depart_time   TEXT,
            depart_iata   TEXT,
            depart_city   TEXT,
            depart_country TEXT,
            depart_key    INTEGER,
            arrival_time  TEXT,
            arrival_iata  TEXT,
            arrival_city  TEXT,
            arrival_country TEXT,
            arrival_key   INTEGER,
            price_total   REAL
        );
    """)

    # now populate it
    curr.execute("""
        INSERT INTO main.combined_offers (
            depart_time,
            depart_iata,
            depart_city,
            depart_country,
            depart_key,
            arrival_time,
            arrival_iata,
            arrival_city,
            arrival_country,
            arrival_key,
            price_total
        )
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
    """)

    # Copy weather tables over
    # create table if not exists
    curr.execute("CREATE TABLE IF NOT EXISTS main.headline AS SELECT * FROM weather_db.headline;")
    curr.execute("CREATE TABLE IF NOT EXISTS main.daily    AS SELECT * FROM weather_db.daily;")

    conn.commit()
    conn.close()

    print(f"Combined DB created at {combined_db} with tables: combined_offers, headline, daily.")

if __name__ == '__main__':
    main()
