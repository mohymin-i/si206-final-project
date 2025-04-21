import sqlite3

def query_offers():
    conn = sqlite3.connect("flight_offers.db")
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM offers
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()

if __name__ == "__main__":
    query_offers()