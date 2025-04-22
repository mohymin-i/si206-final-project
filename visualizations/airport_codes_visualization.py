import matplotlib.pyplot as plt
import sqlite3
import os

def visualize_airports_by_country():
    # Connect to the database
    conn = sqlite3.connect("airport_codes/airport_codes.db")
    cursor = conn.cursor()
    
    target_countries = ['Spain', 'Greece', 'Denmark', 'India', 'Italy']
    
    # Get counts for each country
    counts = []
    for country in target_countries:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM airports 
            WHERE country = ?
        """, (country,))
        count = cursor.fetchone()[0]
        counts.append(count)
        print(f"{country}: {count} airports")
    
    conn.close()
    
    plt.figure(figsize=(10, 6))
    
    # Set color scheme
    colors = ['blue', 'red', 'green', 'purple', 'pink']
    bars = plt.bar(target_countries, counts, color=colors)
    
    # Add count labels on top of each bar
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{count}', ha='center', va='bottom', fontweight='bold')
        
    plt.xlabel('Country', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Airports', fontsize=12, fontweight='bold')
    plt.title('Number of Airports by Country', fontsize=16, fontweight='bold')
    plt.savefig("airport_codes_visualization.png", dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_airports_by_country()