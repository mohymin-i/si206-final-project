import requests
from bs4 import BeautifulSoup
import json

def main():
    url = "https://www.ccra.com/airport-codes/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"request failed -> {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("tbody", class_="row-striping row-hover")
    rows = table.find_all("tr")
    data = {}

    for row in rows:
        city = row.find("td", class_="column-2").text
        country = row.find("td", class_="column-1").text
        code = row.find("td", class_="column-3").text
        data[city] = (code, country)
    

    with open("output.json", "w") as f:
        try:
            json.dump(data, f, indent=2)
        except Exception as e:
            print("failed to write response to file:", e)

if __name__ == "__main__":
    main()