import requests
import json

def main():
    url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    params = {
    "originLocationCode": "DTW",
    "destinationLocationCode": "SEA",
    "departureDate": "2025-05-05",
    "adults": 1,
    "nonStop": "false",
    "max": 10
    }
    headers = {
    'Authorization': f'Bearer h0mkawudvdipGSGTYyCwc8RMkibw'
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    print(data)

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
        except Exception as e:
            print("failed to write response to file:", e)
if __name__ == "__main__":
    main()