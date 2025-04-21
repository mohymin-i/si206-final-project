import matplotlib.pyplot as plt
import json
import numpy as np
import os

def visualize_airport_locations():
    # Load JSON data
    with open("airport_codes/output.json", "r") as f:
        airport_data = json.load(f)

    # If data is a list of airports
    if isinstance(airport_data, list):
        airports = airport_data
    else:
        airports = [airport_data]

    codes = []
    lats = []
    lons = []

    for airport in airports:
        code = airport.get("code") or airport.get("iata")
        lat = airport.get("latitude") or airport.get("lat")
        lon = airport.get("longitude") or airport.get("lon")

        if code and lat and lon:
            codes.append(code)
            try:
                # Convert lat/lon to float if they're strings
                lats.append(float(lat))
                lons.append(float(lon))
            except (ValueError, TypeError):
                continue

    colors = plt.cm.viridis(np.linspace(0, 1, len(codes)))
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor('#F0F8FF')  
    scatter = ax.scatter(lons, lats, c=colors, s=80, alpha=0.7, edgecolor='black')

    # Label each point with the airport code
    for lon, lat, code in zip(lons, lats, codes):
        ax.annotate(code, (lon, lat), fontsize=9, xytext=(3, 3), 
                   textcoords='offset points', fontweight='bold')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_title("Airport Locations on World Map", fontsize=16, fontweight='bold')
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    # Create visualizations directory if it doesn't exist
    if not os.path.exists("visualizations"):
        os.makedirs("visualizations")
        
    plt.savefig("visualizations/airport_locations_map.png")
    plt.show()

if __name__ == "__main__":
    visualize_airport_locations()