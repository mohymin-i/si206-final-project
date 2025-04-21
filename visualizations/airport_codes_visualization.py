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

    # Limit the number of airports (optional)
    airports = airports[:50]  # You can adjust the number

    # Extract data for plotting
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

    # Create a custom colormap for better visualization
    colors = plt.cm.viridis(np.linspace(0, 1, len(codes)))
    
    # Plot map
    fig, ax = plt.subplots(figsize=(12, 8))

    # Add background map image if available
    if os.path.exists("utilities/world_map_background.png"):
        world_map = plt.imread("utilities/world_map_background.png")
        ax.imshow(world_map, extent=[-180, 180, -90, 90], alpha=0.6)
    else:
        # Add a basic outline if no map is available
        ax.set_facecolor('#F0F8FF')  # Light blue background

    # Plot airport locations with varied marker sizes for better visibility
    scatter = ax.scatter(lons, lats, c=colors, s=80, alpha=0.7, edgecolor='black')

    # Label each point with the airport code
    for lon, lat, code in zip(lons, lats, codes):
        ax.annotate(code, (lon, lat), fontsize=9, xytext=(3, 3), 
                   textcoords='offset points', fontweight='bold')

    # Style the plot
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_title("Airport Locations on World Map", fontsize=16, fontweight='bold')
    ax.set_xlabel("Longitude", fontsize=12)
    ax.set_ylabel("Latitude", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Add a colorful border
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
        spine.set_linewidth(2)

    # Save and show plot
    plt.tight_layout()
    
    # Create visualizations directory if it doesn't exist
    if not os.path.exists("visualizations"):
        os.makedirs("visualizations")
        
    # Save to visualizations folder
    plt.savefig("visualizations/airport_locations_map.png", dpi=300, bbox_inches='tight')
    
    # Make sure the plot is displayed
    plt.show()

if __name__ == "__main__":
    # Run the function
    visualize_airport_locations()