import json


def main():
    with open('output.json', 'r') as file:
        json_data = json.load(file)

        table = [
            [
                seg["departure"]["at"],
                seg["departure"]["iataCode"],
                seg["arrival"]["at"],
                seg["arrival"]["iataCode"],
                offer["price"]["total"]
            ]
            for offer in json_data["data"]
            for itin in offer["itineraries"]
            for seg in itin["segments"]
            if len(itin["segments"]) == 1          # keep only direct flights
        ]
        for i in range(0, len(table)):
            print(table[i])

if __name__ == "__main__":
    main()