from db_tools import create_connection, get_all_schemas

print("=======")
print("testing out create connection")
connection = create_connection()
print(connection)

print("=======")
print("testing out get_all_schemas")
schema = get_all_schemas()
print(schema)
