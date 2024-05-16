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


# sql_query = "DROP TABLE IF EXISTS `device`;"
# cursor.execute(sql_query)
# create_table_query = """CREATE TABLE `device` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `device_name` varchar(45) DEFAULT NULL,
#   `user_id` int DEFAULT NULL,
#   `timestamp` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) """
# cursor.execute(create_table_query)
# print("Table 'enterprise' created successfully.")

# sql_query = "DROP TABLE IF EXISTS `dpth_reading`;"
# cursor.execute(sql_query)
# create_table_query = """CREATE TABLE `dpth_reading` (
#   id int NOT NULL AUTO_INCREMENT,
#   `device_name` varchar(45) DEFAULT NULL,
#   `dp_value` int DEFAULT NULL,
#   `temp_value` float DEFAULT NULL,
#   `hum_value` int DEFAULT NULL,
#   `timestamp` datetime DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) """
# cursor.execute(create_table_query)
# print("Table 'dpth_reading' created successfully.")

# sql_query = "DROP TABLE IF EXISTS `enterprise`;"
# cursor.execute(sql_query)
# create_table_query = """CREATE TABLE `enterprise` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `enterprisename` varchar(255) DEFAULT NULL,
#   `username` varchar(255) DEFAULT NULL,
#   `password` varchar(255) DEFAULT NULL,
#   `email` varchar(255) DEFAULT NULL,
#   `mobile` varchar(255) DEFAULT NULL,
#   `logopath` varchar(256) DEFAULT NULL,
#   `admin` varchar(255) DEFAULT NULL,
#   `datecreated` varchar(45) DEFAULT NULL,
#   `dateupdated` varchar(45) DEFAULT NULL,
#   `datedeleted` varchar(45) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# ) """
# cursor.execute(create_table_query)
# print("Table 'dpth_reading' created successfully.")
    
# sql_query = "DROP TABLE IF EXISTS `roles`;"
# cursor.execute(sql_query)
# create_table_query = """CREATE TABLE roles (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     role VARCHAR(255),
#     active BOOLEAN
# );"""

# cursor.execute(create_table_query)
# print("Table 'roles' created successfully.")

# sql_query = "DROP TABLE IF EXISTS `role_access`;"
# cursor.execute(sql_query)
# create_table_query = """CREATE TABLE role_access (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     role_id INT,
#     user_id INT,
#     FOREIGN KEY (role_id) REFERENCES roles(id),
#     FOREIGN KEY (user_id) REFERENCES enterprise(id)
# );"""

# cursor.execute(create_table_query)
# print("Table 'role_access' created successfully.")