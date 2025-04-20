import json
import sqlite3
import os

def clean(airportName):
    # Cleans names, helper function
    return airportName.strip().strip("\u00a0")

def main():
    # get local path
    here = os.path.dirname(__file__)
    json_path = os.path.join(here, 'output.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create database file
    db_path = os.path.join(here, 'airport_codes.db')
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()

    # create table
    curr.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            iata_code TEXT PRIMARY KEY,
            city      TEXT NOT NULL,
            country   TEXT NOT NULL
        );''')
    conn.commit()

    # insert every entry
    count = 0
    for city, entries in data.items():
        city_clean = clean(city)
        # some cities may have multiple airports
        # alexandria, Egypt, for instance has airports ALY and HBE
        for code, country in entries:
            code_clean = clean(code)
            country_clean = clean(country)
            curr.execute(
                'INSERT OR REPLACE INTO airports (iata_code, city, country) VALUES (?, ?, ?)',
                (code_clean, city_clean, country_clean)
            )
            count += 1

    conn.commit()
    conn.close()

    print(f"Inserted {count} airport records into {db_path}")

if __name__ == '__main__':
    main()
