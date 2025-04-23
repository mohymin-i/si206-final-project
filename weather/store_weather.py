import json
import sqlite3
import os
import sys
import requests

API_KEY="yAuYwbDrgKDZD0lNLHGeKL5TMNulN4bS"

def main(location_code, forecast_type):
    # load the weather data
    here = os.path.dirname(__file__)
    json_path = os.path.join(here, 'weather_output.json')

    if forecast_type == "hourly":
        url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_code}'
    else:
        url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}'

    params = {
    "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    # Create (or open) the SQLite database
    db_path = os.path.join(os.path.dirname(here), 'database.db')
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()

    # create headline table
    # gets data for today 
    curr.execute('''
        CREATE TABLE IF NOT EXISTS headline (
            effective_date TEXT,
            severity       INTEGER,
            text           TEXT,
            category       TEXT,
            end_date       TEXT
        );
    ''')

    # daily forecasts
    curr.execute('''
        CREATE TABLE IF NOT EXISTS daily (
            forecast_date            TEXT,
            epoch_date               INTEGER,
            min_value                REAL,
            max_value                REAL,
            day_phrase               TEXT,
            day_has_precipitation    TEXT,
            day_precip_type          TEXT,
            day_precip_intensity     TEXT,
            night_phrase             TEXT,
            night_has_precipitation  TEXT,
            night_precip_type        TEXT,
            night_precip_intensity   TEXT
        );
    ''')
    conn.commit()

    # insert stuff into headline 
    # only a single row (today's forecast)
    headline = data.get('Headline', {})
    curr.execute(
        '''INSERT INTO headline (effective_date, severity, text, category, end_date)
        VALUES (?, ?, ?, ?, ?)''',
        (
            headline.get('EffectiveDate'),
            headline.get('Severity'),
            headline.get('Text'),
            headline.get('Category'),
            headline.get('EndDate')
        )
    )

    # insert stuff into daily

    for fcast in data.get('DailyForecasts', []):
        temp = fcast.get('Temperature', {})
        minimum = temp.get('Minimum', {})
        maximum = temp.get('Maximum', {})
        day = fcast.get('Day', {})
        night = fcast.get('Night', {})

        # Convert booleans to "true"/"false"
        day_has = 'true' if day.get('HasPrecipitation', False) else 'false'
        night_has = 'true' if night.get('HasPrecipitation', False) else 'false'

        curr.execute(
            '''INSERT INTO daily (
                forecast_date, epoch_date,
                min_value, max_value,
                day_phrase, day_has_precipitation, day_precip_type, day_precip_intensity,
                night_phrase, night_has_precipitation, night_precip_type, night_precip_intensity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                fcast.get('Date'),
                fcast.get('EpochDate'),
                minimum.get('Value'),
                maximum.get('Value'),
                day.get('IconPhrase'),
                day_has,
                day.get('PrecipitationType'),
                day.get('PrecipitationIntensity'),
                night.get('IconPhrase'),
                night_has,
                night.get('PrecipitationType'),
                night.get('PrecipitationIntensity')
            )
        )

    conn.commit()
    conn.close()
    print(f"Inserted weather data into {db_path}")

if __name__ == "__main__":
    try:
        code, forecast_type = sys.argv[1:3]
    except (IndexError, ValueError):
        print("""Usage: python store_weather.py <LOCATION_CODE> <hourly || daily>
Ex Los Angeles: $python store_weather.py 347625 daily
See comment in this file for location codes.""")
        sys.exit(1)
    if forecast_type != "hourly" and forecast_type != "daily":
        print("Error, unknown forecast type, only use 'daily' or 'hourly'")
        sys.exit(1)
    main(code, forecast_type)