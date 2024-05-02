import pyorient

from utils import get_records


client = pyorient.OrientDB("localhost", 2424)
client.connect("root", "rootpwd")


db_name = "test"


if not client.db_exists(db_name):
    client.db_create(db_name)


session_id = client.db_open(db_name, "root", "rootpwd")
print(session_id)


class_name = "body"
# client.command("CREATE CLASS {}".format(class_name))


# client.command("CREATE PROPERTY {}.body STRING".format(class_name))


record_data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]


for data in record_data:
    command = "INSERT INTO {} SET ".format(class_name)
    command += ", ".join("{} = '{}'".format(k, v) for k, v in data.items())
    client.command(command)


print(client.db_size())


query = "SELECT FROM {}".format(class_name)
result = client.query(query)


print("Retrieved data:")
for record in result:
    print(record)
    print("Name: {}, Age: {}".format(record.name, record.age))

db_name = "abc"


if not client.db_exists(db_name):
    client.db_create(db_name)


session_id = client.db_open(db_name, "root", "rootpwd")
print(session_id)


class_name = "body"
# client.command("CREATE CLASS {}".format(class_name))


# client.command("CREATE PROPERTY {}.body STRING".format(class_name))


record_data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]


for data in record_data:
    command = "INSERT INTO {} SET ".format(class_name)
    command += ", ".join("{} = '{}'".format(k, v) for k, v in data.items())
    client.command(command)


print(client.db_size())

db_name = "test"

session_id = client.db_open(db_name, "root", "rootpwd")
print(client.db_size())


client.db_close(session_id)
client.close()