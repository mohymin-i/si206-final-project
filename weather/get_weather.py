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

def main(location_code):
    load_dotenv()

    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_code}'
    params = {
    "apikey": os.getenv("ACCUWEATHER_API_KEY")
    }

    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
        except Exception as e:
            print("failed to write response to file:", e)
    return


if __name__ == "__main__":
    try:
        code = sys.argv[1]
    except (IndexError, ValueError):
        print("""Usage: python get_weather.py <LOCATION CODE>
Ex Los Angeles: $python get_weather.py 347625
See comment in this file for location codes.""")
        sys.exit(1)
    main(code)