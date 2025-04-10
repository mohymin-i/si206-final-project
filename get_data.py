import requests
import json
import matplotlib.pyplot as plt
import sqlite3

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

def get_flight_prices(table, conn):
    #load json data
    with open('output.json', 'r') as file:
        flight_data = json.load(file)
    
    cursor = conn.cursor()

    for entry in flight_data:
        insert_query = f"""INSERT INTO {table} (flight, price, origin, destination)
        VALUES (?, ?, ?, ?)
    """

        cursor.execute(insert_query, (
            entry["flight"],
            entry["price"],
            entry["origin"],
            entry["destination"]
        ))
    
    flight_names = [flight['flight'] for flight in flight_data]
    flight_prices = [flight['price'] for flight in flight_data]

    plt.figure(figsize=(8,5))
    plt.hist(flight_prices, bins=10, color="blue", edgecolor = "black")
    plt.title("Distribution of Flight Prices")
    plt.xlabel("Price ($)")
    plt.ylabel("Number of Flights")
    plt.grid(axis='y', linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


    

if __name__ == "__main__":
    main()