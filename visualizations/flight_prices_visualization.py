import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

def visualize_average_flight_prices():
    conn = sqlite3.connect("flights/flight_offers.db")

    # Get date and average price
    query = """
    SELECT date(depart_time) AS flight_date, AVG(price_total) AS avg_price
    FROM offers
    GROUP BY flight_date
    ORDER BY flight_date
    LIMIT 5
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    dates = df['flight_date']
    prices = df['avg_price']

    # Create the line graph
    fig, ax = plt.subplots()
    ax.plot(dates, prices, label="Avg. Price", marker='o', color="green")

    for date, price in zip(dates, prices):
        ax.text(date, price + 5, f"${price:.2f}", ha='center', fontsize=9)
    ax.set_title("Average Flight Prices Over 5 Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate()
    plt.savefig("flight_prices_visualization.png")
    plt.show()

visualize_average_flight_prices()
