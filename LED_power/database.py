import sqlite3

def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('led_power.db')
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    print("Connected to database successfully")

    cursor.execute('DROP TABLE IF EXISTS ot_device_info')
        
    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS power
                      (id INTEGER PRIMARY KEY, name TEXT, power INTEGER)''')
    
    print("Created table successfully!")
    # Save (commit) the changes
    conn.commit()
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    create_database()