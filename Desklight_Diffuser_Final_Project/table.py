import sqlite3

conn = sqlite3.connect('scheduling.db')  # Corrected database filename
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scheduling (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        SrNo TEXT,
        ScheduleStartTime TEXT,
        ScheduleEndTime TEXT,
        scheduling INT
    )
''')
    
    # Split the input SrNo string by comma and insert each serial number into the database
conn.commit()
conn.close()