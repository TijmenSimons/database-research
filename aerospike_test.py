import aerospike

# Initialize the Aerospike client
config = {
    'hosts': [('localhost', 3000)]  # Assuming Aerospike server is running locally on port 3000
}
client = aerospike.client(config).connect()

namespace = "test"
set_name = "example_set"

# Define a key for the record
key = ('test', 'example_set', 'example_key')

# Define some sample data to put into the database
data = {
    'name': 'John Doe',
    'age': 30,
    'city': 'New York'
}

# Put data into the database
client.put(key, data)
client.remove(key)

# Retrieve data from the database
(key, metadata, record) = client.get(key)


# Print the retrieved record
print("Retrieved Record:")
print(record)

# Close the connection to the Aerospike cluster
client.close()