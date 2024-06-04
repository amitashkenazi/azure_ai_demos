from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv
import uuid
from pprint import pprint 
from azure.cosmos.partition_key import PartitionKey

# Load the .env file
load_dotenv()

# Initialize a Cosmos Client
url = os.environ['COSMOS_LINK'] 
key = os.environ['COSMOS_KEY'] 
print(f"URL: {url}")
print(f"KEY: {key}")
client = CosmosClient(url, credential=key)
print("Client initialized successfully!")
# Select a database
database_name = 'faqdemo'
database = client.get_database_client(database_name)

# Select a container
container_name = 'faqdemo'
container = database.get_container_client(container_name)
print(f'Container {container_name} selected successfully!')
def check_database(database_name):
# check if database exists and create if it doesn't
    try:
        print(f"Checking if database {database_name} exists...")
        database = client.get_database_client(database_name)
    except Exception as e:
        print(f"Database {database_name} does not exist. Creating...")
        database = client.create_database_if_not_exists(id=database_name)
        print(f"Database {database_name} created successfully!")
    return database

def check_container(container_name):
# check if container exists and create if it doesn't
    try:
        print(f"Checking if container {container_name} exists...")
        container = database.get_container_client(container_name)
    except Exception as e:
        print(f"Container {container_name} does not exist. Creating...")
        container = database.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path="/id"))
        print(f"Container {container_name} created successfully!")
    return container

def store(test_result):
    test_result["id"] = str(uuid.uuid4())
    container.upsert_item(test_result)
    print("Document uploaded successfully!")

def get():
    return list(container.read_all_items())

def delete_item(item_id):
    container.delete_item(item_id, item_id)
    print("Document deleted successfully!")

def delete_all_matches():
    for item in container.read_all_items():
        item_id = item['id']
        print(item_id)
        partition_key_value = item['id']  # replace with your partition key attribute
        container.delete_item(item, partition_key_value)
        
    print("All documents deleted successfully!")

def update_item(item_id, test_result):
    container.upsert_item(test_result)
    print("Document updated successfully!")

if __name__ == "__main__":
    import pandas as pd
    docs = get()
    # delete all docs
    for doc in docs:
        delete_item(doc['id'])
    
    df = pd.read_csv("data/faqs.csv")

    for i, row in df.iterrows():
        test_result = {
            "question": row["question"],
            "answer": row["answer"],
            "url": "https://faq.demo.com",
            "title": "FAQ",
            "file_name": "faqs.csv"
        }
        store(test_result)
        print(i, row["question"], row["answer"])