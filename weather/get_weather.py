"""Get the top 50 city codes for the weather API"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

"""
Location Codes

Chicago -> 348308
Seattle -> 351409
New York -> 349727
Los Angeles -> 347625
San Francisco -> 347629
Miami -> 347936
Dallas -> 351194
"""

def main(location_code, forecast_type):
    load_dotenv()

    # Different APIs to call from lowkey just need more rows of data
    if forecast_type == "hourly":
        url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_code}'
    else:
        url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}'

    params = {
    "apikey": os.getenv("ACCUWEATHER_API_KEY")
    }

    response = requests.get(url, params=params)
    data = response.json()
    #print(data)

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
        except Exception as e:
            print("failed to write response to file:", e)
    return


if __name__ == "__main__":
    try:
        code, forecast_type = sys.argv[1:3]
    except (IndexError, ValueError):
        print("""Usage: python get_weather.py <LOCATION_CODE> <hourly || daily>
Ex Los Angeles: $python get_weather.py 347625 daily
See comment in this file for location codes.""")
        sys.exit(1)
    if forecast_type != "hourly" and forecast_type != "daily":
        print("Error, unknown forecast type, only use 'daily' or 'hourly'")
        sys.exit(1)
    main(code, forecast_type)