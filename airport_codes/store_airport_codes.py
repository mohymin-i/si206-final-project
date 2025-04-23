import json
import sqlite3
import os

def clean(airportName):
    # Cleans names, helper function
    return airportName.strip().strip("\u00a0")

def iataToInt(iata):
    integerKey = 0
    for char in iata[:3]:
        integerKey *= 100
        integerKey += ord(char)
    return integerKey

def main():
    # get local path
    here = os.path.dirname(__file__)
    json_path = os.path.join(here, 'output.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create database file
    db_path = os.path.join(os.path.dirname(here), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON") 
    curr = conn.cursor()

    # countires table
    curr.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );''')

    # create airports table (modified to use country
    curr.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            iata_code TEXT PRIMARY KEY,
            integer_key INTEGER,
            city      TEXT NOT NULL,
            country INTEGER NOT NULL,
            FOREIGN KEY (country) REFERENCES countries(id)
        );''')
    conn.commit()

    countries = set() # avoid duplciates
    for city, entries in data.items():
        for code, country in entries:
            countries.add(clean(country))
    for country in countries:
        curr.execute(
            'INSERT OR IGNORE INTO countries (name) VALUES (?)',
            (country,)
        )

    curr.execute('SELECT id, name FROM countries')
    country_id_lookup = {name: cid for cid, name in curr.fetchall()}

    # insert every entry
    count = 0
    for city, entries in data.items():
        city_clean = clean(city)
        # some cities may have multiple airports
        # alexandria, Egypt, for instance has airports ALY and HBE
        for code, country in entries:
            cleanedCode = clean(code)
            cleanedCountry = clean(country)
            curr.execute(
                'INSERT OR REPLACE INTO airports (iata_code, integer_key, city, country) VALUES (?, ?, ?, ?)',
                (cleanedCode, iataToInt(cleanedCode), city_clean, country_id_lookup[cleanedCountry])
            )
            count += 1

    conn.commit()
    conn.close()

    print(f"Inserted {count} airport records into {db_path}")

if __name__ == '__main__':
    main()
