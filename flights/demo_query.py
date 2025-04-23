import sqlite3
import os

def fetch_top_5_cheapest_flights():
    here = os.path.dirname(__file__)
    db_path = os.path.join(here, os.pardir, 'database.db')

    conn = sqlite3.connect(db_path)
    curr = conn.cursor()

    query_top_5 = """
    SELECT 
        o.depart_time, 
        o.arrival_time, 
        o.price_total, 
        d.iata_code AS depart_code, 
        d.city AS depart_city, 
        d.country AS depart_country, 
        a.iata_code AS arrival_code, 
        a.city AS arrival_city, 
        a.country AS arrival_country
    FROM offers o
    JOIN airports d ON o.depart_key = d.integer_key
    JOIN airports a ON o.arrival_key = a.integer_key
    ORDER BY o.price_total ASC
    LIMIT 5;
    """

    curr.execute(query_top_5)
    results = curr.fetchall()

    curr.execute("SELECT AVG(price_total) FROM offers;")
    avg_price = curr.fetchone()[0]
    conn.close()

    output_path = os.path.join(here, 'top_5_cheapest_flights.txt')
    with open(output_path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(f"Depart: {row[3]} ({row[4]}, {row[5]}) at {row[0]}\n")
            f.write(f"Arrive: {row[6]} ({row[7]}, {row[8]}) at {row[1]}\n")
            f.write(f"Price: ${row[2]:.2f}\n")
            f.write("-" * 50 + "\n")
        f.write(f"\nAverage price of all flights in database: ${avg_price:.2f}\n")

    print(f"Top 5 cheapest flights and average price written to: {output_path}")

if __name__ == "__main__":
    fetch_top_5_cheapest_flights()