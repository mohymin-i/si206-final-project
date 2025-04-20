import matplotlib.pyplot as plt
import json
from datetime import datetime

# Get min and max weather temperature function
def get_weather_min_max():
    #Load JSON data
    with open("weather/weather_output.json", "r") as f:
        weather_data = json.load(f)

    forecasts = weather_data['DailyForecasts']

    dates = []
    min_temps = []
    max_temps = []

    #For loop to loop through forecast data
    for forecast in forecasts:
        #Collect and properly format date
        date_str = forecast["Date"]
        date_obj = datetime.fromisoformat(date_str[:-6]) #Fixes timezone differences
        dates.append(date_obj.strftime("%b %d"))

        #Collect min and max temps
        min_temp = forecast["Temperature"]["Minimum"]['Value']
        max_temp = forecast["Temperature"]["Maximum"]['Value']

        min_temps.append(min_temp)
        max_temps.append(max_temp)

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