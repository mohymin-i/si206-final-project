import subprocess
import sys
from datetime import date

# Usage
# run this code
# change the airports list to get different flights


# routes we get data for
def generateRoutes(airports):
    routes = []
    for start in airports:
        for end in airports:
            if (start != end):
                routes.append((start, end))
    return routes

# departing date
departingDate = "2025-06-01"

# run the command
def run(cmd):
    print("---->", " ".join(cmd)) # comment out if ouptut is annoying
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        print("ERROR:", result.stderr)
        sys.exit(1)
    else:
        print(result.stdout.strip())

def main():
    airports = [
        "LAX", 
        "JFK", 
        "DTW",
        "ATL",
        "LBR",
        "SEA",
        "FCO",
        "DEN",
        "MEX",
        # "SFO",
        # "ORD",
        # "YYZ",
        # "BUF",
        # "CLE",
        # "ANC",
        # "CDG",
        # "BER"
    ] 

    routes = generateRoutes(airports)
    print("Finding flights between", len(routes), "pairs of airports")
    for origin, dest in routes:
        # fetch data and store it in the json
        run(["python3", "flights/get_flights.py", origin, dest, departingDate])
        # store the flights
        run(["python3", "flights/store_flights.py"])
    # print when done
    print("Done populating offers.")

if __name__ == "__main__":
    main()
