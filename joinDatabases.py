import subprocess
import os
import sys

# simply run this python file to get the database
# to change the items in the database, go to 

def build_database(path):
    print(f"Running: {path}")
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {path}:\n{result.stderr}")
        sys.exit(1)
    else:
        print(f"Output from {path}:\n{result.stdout}")

def main():
    here = os.path.dirname(__file__)

    filePaths = [
        # file paths to python files for the APIs
        # each of these files takes data and creates a database
        # populate_database makes repeated calls to the flights API (each call takes in 10 items or less)
        # airport_codes is scraped from a website
        # store_weather makes a single API call
        os.path.join(here, "flights", "populate_database.py"),
        os.path.join(here, "airport_codes", "store_airport_codes.py"),
        os.path.join(here, "weather", "store_weather.py")
    ]

    for file in filePaths:
        build_database(file)

    print("Database Created")

if __name__ == "__main__":
    main()
