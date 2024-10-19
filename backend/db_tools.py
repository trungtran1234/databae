import mysql.connector
from mysql.connector import Error
import json 
import os

# helper function to create the connection to the database
# based on credentials in db_credentials.json
def create_connection():
    connection = None

    if not os.path.abspath('db_credentials.json'):
        print("no db credentials found")
        return None
    
    with open('db_credentials.json') as f:
        data = json.load(f)
        host_name = data["host_name"]
        user_name = data["user_name"]
        user_password = data["user_password"]
        port = data["port"]
        db_name = data["db_name"]
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                port=port,
                database=db_name
            )
            print("Connection to MySQL DB successful")
            if connection:
                return connection
            else:
                return None
        except Error as e:
            print(f"The error '{e}' occurred")
            return None

    return connection

# helper function that checks whether the db connection is valid
# and saves it in db_credentials.json
# !!! for now, ssl has to be disabled on the database side
def check_and_add_db_credentials(host_name, user_name, user_password, port, db_name): 
    connection = None 
    try:
        print("connecting")
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            port=port,
            database=db_name,
            ssl_disabled=True
        )
        if connection:
            print("Connection to MySQL DB successful")
            with open("db_credentials.json", "w") as f:
                json.dump({"host_name": host_name, 
                           "user_name": user_name, 
                           "user_password": user_password, 
                           "port": port, 
                           "db_name": db_name}, 
                        f)
            close_connection(connection)
            return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False

# helper function to close the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed")

# helper function to grab all schemas from the database
# it will return a dictionary of the format
# {
# table_name: [ {}'column_name': 'example_name', 'data_type': 'example_data_type' ],
# table_name2: [ 'column_name_2': 'example_name', 'data_type': 'example_data_type' ],
# }
def get_all_schemas():
    conn = create_connection()
    if not conn:
        return {}
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s", 
            [conn.database]
        )
        schemas = cursor.fetchall()
    finally:
        cursor.close() 
        conn.close() 

    if schemas:
        dict_of_data_schema = {}
        for schema in schemas:
            if schema[0] not in dict_of_data_schema:
                dict_of_data_schema[schema[0]] = []
            dict_of_data_schema[schema[0]].append({"column_name": schema[1], "data_type": schema[2]})
        return dict_of_data_schema
    else:
        return {}