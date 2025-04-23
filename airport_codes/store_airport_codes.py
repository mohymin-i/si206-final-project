import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import json

def clean(airportName):
    return airportName.strip().strip("\u00a0")

def iataToInt(iata):
    integerKey = 0
    for char in iata[:3]:
        integerKey *= 100
        integerKey += ord(char)
    return integerKey

def main():
    here = os.path.dirname(__file__)

    url = "https://www.ccra.com/airport-codes/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"request failed -> {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("tbody", class_="row-striping row-hover")
    rows = table.find_all("tr")
    data = {}
    for row in rows:
        city = row.find("td", class_="column-1").text
        country = row.find("td", class_="column-2").text
        code = row.find("td", class_="column-3").text
        if city in data:
            data[city].append((code, country))
        else:
            data[city] = [(code, country)]

    db_path = os.path.join(os.path.dirname(here), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON") 
    curr = conn.cursor()

    curr.execute('''
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );''')

    curr.execute('''
        CREATE TABLE IF NOT EXISTS airports (
            iata_code TEXT PRIMARY KEY,
            integer_key INTEGER,
            city      TEXT NOT NULL,
            country INTEGER NOT NULL,
            FOREIGN KEY (country) REFERENCES countries(id)
        );''')
    conn.commit()

    curr.execute('SELECT COUNT(*) FROM countries')
    current_country_count = curr.fetchone()[0]
    country_insert_limit = 25
    countries = sorted({clean(country) for entries in data.values() for _, country in entries})
    inserted_countries = 0
    for country in countries:
        if current_country_count > 0:
            current_country_count -= 1
            continue
        if inserted_countries >= country_insert_limit:
            break
        curr.execute(
            'INSERT OR IGNORE INTO countries (name) VALUES (?)',
            (country,)
        )
        inserted_countries += 1
    print(f"Inserted {inserted_countries} countries into {db_path}")

    # all countries need to be added before this code will work
    if inserted_countries == 0:
        curr.execute('SELECT id, name FROM countries')
        country_id_lookup = {name: cid for cid, name in curr.fetchall()}

        curr.execute('SELECT COUNT(*) FROM airports')
        current_airport_count = curr.fetchone()[0]
        airport_insert_limit = 25
        inserted_airports = 0
        count = 0
        for city, entries in data.items():
            if inserted_airports >= airport_insert_limit:
                break
            city_clean = clean(city)
            for code, country in entries:
                if inserted_airports >= airport_insert_limit:
                    break
                if current_airport_count > 0:
                    current_airport_count -= 1
                    continue
                cleanedCode = clean(code)
                cleanedCountry = clean(country)
                curr.execute(
                    'INSERT OR REPLACE INTO airports (iata_code, integer_key, city, country) VALUES (?, ?, ?, ?)',
                    (cleanedCode, iataToInt(cleanedCode), city_clean, country_id_lookup[cleanedCountry])
                )
                inserted_airports += 1
                count += 1
        print(f"Inserted {count} airport records into {db_path}")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()