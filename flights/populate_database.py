import subprocess
import sys
from datetime import date

# routes we get data for
routes = [
    ("JFK","LAX"),
    ("JFK","ORD"),
    ("JFK","MIA"),
    ("LAX","SEA"),
    ("LAX","DEN"),
    ("ORD","DFW"),
    ("MIA","ATL"),
    ("SEA","SFO"),
    ("DEN","PHX"),
    ("DFW","BOS"),
]

# departing date
departingDate = "2025-06-01"

# run the command
def run(cmd):
    print("---->", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        print("ERROR:", result.stderr)
        sys.exit(1)
    else:
        print(result.stdout.strip())

def main():
    for origin, dest in routes:
        # fetch data and store it in the json
        run(["python3", "get_flights.py", origin, dest, departingDate])
        # store the flights
        run(["python3", "store_flights.py"])
    # print when done
    print("Done populating offers.")

if __name__ == "__main__":
    main()
