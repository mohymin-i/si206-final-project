import matplotlib.pyplot as plt
import json

# Average flight prices for 5 days for a certain destination

def get_flight_prices(table, conn):
    #load json data
    with open('output.json', 'r') as f:
        flight_data = json.load(f)
    
    prices = flight_data["price"]

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