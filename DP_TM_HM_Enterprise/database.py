import mysql.connector

# configure the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="status_control"
)
cursor = mydb.cursor()

if mydb.is_connected():
    print("Connected to the database.")
    cursor = mydb.cursor()
else:
    print("Failed to connect to the database.")

# sql_query = "DROP TABLE IF EXISTS enterprise"
# 
# create_table_query = """
#         CREATE TABLE enterprise (
#             id INT NOT NULL AUTO_INCREMENT,
#             enterprisename VARCHAR(255) DEFAULT NULL,
#             username VARCHAR(255) DEFAULT NULL,
#             password VARCHAR(255) DEFAULT NULL,
#             email VARCHAR(255) DEFAULT NULL,
#             mobile VARCHAR(255) DEFAULT NULL,
#             logopath VARCHAR(256) DEFAULT NULL,
#             admin VARCHAR(255) DEFAULT NULL,
#             datecreated VARCHAR(45) DEFAULT NULL,
#             dateupdated VARCHAR(45) DEFAULT NULL,
#             datedeleted VARCHAR(45) DEFAULT NULL,
#             PRIMARY KEY (id)
#         )
#         """
        
# cursor.execute(create_table_query)
# print("Table 'enterprise' created successfully.")