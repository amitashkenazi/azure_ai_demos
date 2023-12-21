from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv
import uuid
from pprint import pprint 

# Load the .env file
load_dotenv()

# Initialize a Cosmos Client
url = os.environ['COSMOS_LINK'] 
key = os.environ['COSMOS_KEY'] 
client = CosmosClient(url, credential=key)

# Select a database
database_name = 'faqdemo'
database = client.get_database_client(database_name)

# Select a container
container_name = 'faqdemo'
container = database.get_container_client(container_name)

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
    df = pd.read_csv("data/faqs.csv")

    for i, row in df.iterrows():
        test_result = {
            "question": row["question"],
            "answer": row["answer"]
        }
        store(test_result)
        print(i, row["question"], row["answer"])