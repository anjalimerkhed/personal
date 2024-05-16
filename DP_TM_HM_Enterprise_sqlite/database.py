import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('dpth_enterprise.db',check_same_thread=False)
cursor = conn.cursor()
print("Connected to database successfully")

# # Execute the query to drop the enterprise table if it exists
# cursor.execute("""DROP TABLE IF EXISTS enterprise""")

# # Execute the query to drop the device table if it exists
# cursor.execute("""DROP TABLE IF EXISTS device""")

# # Execute the query to drop the dpth_readings table if it exists
# cursor.execute("""DROP TABLE IF EXISTS dpth_readings""")

# # SQL query to create the enterprise table
# create_enterprise_table_query = """
#         CREATE TABLE enterprise (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             enterprisename VARCHAR(255) DEFAULT NULL,
#             username VARCHAR(255) DEFAULT NULL,
#             password VARCHAR(255) DEFAULT NULL,
#             email VARCHAR(255) DEFAULT NULL,
#             mobile VARCHAR(255) DEFAULT NULL,
#             logopath VARCHAR(256) DEFAULT NULL,
#             admin VARCHAR(255) DEFAULT NULL,
#             datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             dateupdated ,
#             datedeleted
#         )
#  """
# Execute the query to create the enterprise table
# cursor.execute(create_enterprise_table_query)
# print("Table enterprise created successfully!")

# # SQL query to create the device table
# create_device_table_query = """
#         CREATE TABLE device (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             device_name VARCHAR(255) DEFAULT NULL,
#             user_id INTEGER,
#             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (user_id) REFERENCES enterprise(id)
#         )
# """
# # Execute the query to create the device table
# cursor.execute(create_device_table_query)
# print("Table device created successfully!")

# # SQL query to create the dpth_readings table
# create_dpth_readings_table_query = """
#         CREATE TABLE dpth_readings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             device_name VARCHAR(255) DEFAULT NULL,
#             dp_value INTEGER,
#             temp_value REAL,
#             hum_value INTEGER,
#             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
# """
# # Execute the query to create the dpth_readings table
# cursor.execute(create_dpth_readings_table_query)
# print("Table dpth_readings created successfully!")

# Commit the transaction and close the connection
# conn.commit()
# conn.close()
