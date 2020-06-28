from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family
import requests
import json

# Initialize the Cosmos client
endpoint = "https://neha-ashna-sql.documents.azure.com:443/"
key = 'OHGmnmv3z53vl7kn2r17rN9Suu20osDAfl4ALISjWO58biTjiLuldIdfsRdBA6IRnZFcczu7nrSEpHry6rLZew=='

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'AzureSampleFamilyDatabase'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'FamilyContainer'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/lastName"),
    offer_throughput=400
)
# </create_container_if_not_exists>


# Add items to the container
family_items_to_create = [family.get_andersen_family_item(), family.get_johnson_family_item(), family.get_smith_family_item(), family.get_wakefield_family_item()]

 # <create_item>
for family_item in family_items_to_create:
    container.create_item(body=family_item)
# </create_item>

# Read items (key value lookups by partition key and id, aka point reads)
# <read_item>
for family in family_items_to_create:
    item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
    print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
# </read_item>

# Query these items using the SQL query syntax. 
# Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
# <query_items>
query = "SELECT * FROM c WHERE c.lastName IN ('Wakefield', 'Andersen')"

items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
# </query_items>


from flask import Flask
app = Flask(__name__)
@app.route("/")

def index():

    url1="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/delivery_quotes"
    url2="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/deliveries"

    #https://postmates.com/developer/docs/#resources__delivery__create-delivery
  
  #This is the API KEY: ea6f0581-b447-459e-98cc-5c7b22a27335
    
    pickup_address = "9 Bernadette Circle, Monmouth Junction, 08852"
    dropoff_address = "30 Providence Blvd, Kendall Park NJ, 08824"
    quote_params = {
      "dropoff_address": dropoff_address,
      "pickup_address": pickup_address
    }

    quote_req = requests.post(url1, params=quote_params, auth=('ea6f0581-b447-459e-98cc-5c7b22a27335', ''))

    if quote_req.status_code != 200:
      print("Error:", quote_req.status_code)

    quote_id = quote_req.json()["id"]

    pickup_name = "Ashna's house"
    pickup_phone_number = "7324229194"
    dropoff_name = "Neha"
    dropoff_phone_number = "6098656754"
    manifest = "test items"

    manifest_items = []
    #manifest_items.append(manifest_item)

    delivery_params = {
      "dropoff_address": dropoff_address,
      "dropoff_name": dropoff_name,
      "dropoff_phone_number": dropoff_phone_number,
      "manifest": manifest,
      "manifest_items": manifest_items,
      "pickup_address": pickup_address,
      "pickup_name": pickup_name,
      "pickup_phone_number": pickup_phone_number,
      "quote_id": quote_id
    }

    delivery_req = requests.post(url2, params=delivery_params, auth=('ea6f0581-b447-459e-98cc-5c7b22a27335', ''))
    return "Hello World!"