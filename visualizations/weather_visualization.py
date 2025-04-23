import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import json
from datetime import datetime

# Get min and max weather temperature function
def get_weather_min_max():
    #Connect to weather database
    conn = sqlite3.connect("database.db")
    
    query = """
    SELECT
        forecast_date,
        min_value,
        max_value
    FROM daily
    GROUP BY forecast_date
    ORDER BY forecast_date
    LIMIT 5
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    dates = []
    min_temps = df['min_value'].tolist()
    max_temps = df['max_value'].tolist()

    #Process dates with timezones
    for date_str in df['forecast_date']:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        dates.append(date_obj.strftime("%b %d"))
   

    fig, ax = plt.subplots()

    #Plot for line chart
    fig, ax = plt.subplots()
    ax.plot(dates, min_temps, label="Minimum Temperature", marker = 'o', color = "red")
    ax.plot(dates, max_temps, label="Maximum Temperature", marker = 'o', color = "blue")
    ax.fill_between(dates, min_temps, max_temps, color = "lightgray", alpha = 0.3)
    ax.set_title("Highs and Lows in Five Day Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°F)")
    ax.legend()
    ax.grid(True)
    plt.savefig("weather_visualization.png")
    plt.show()

get_weather_min_max()

