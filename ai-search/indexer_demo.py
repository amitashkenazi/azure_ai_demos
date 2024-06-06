import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataSourceConnection,
    SearchIndexer,
    FieldMapping
)
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

# Azure Cognitive Search and Cosmos DB configuration
AI_SEARCH_SERVICE = os.getenv("AI_SEARCH_SERVICE")
AI_SEARCH_KEY = os.getenv("AI_SEARCH_KEY")
COSMOS_LINK = os.getenv("COSMOS_LINK")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")
INDEX_NAME = os.getenv("AI_SEARCH_INDEX_NAME")

# Initialize clients
search_indexer_client = SearchIndexerClient(endpoint=f"https://{AI_SEARCH_SERVICE}.search.windows.net",
                                            credential=AzureKeyCredential(AI_SEARCH_KEY))
cosmos_client = CosmosClient(COSMOS_LINK, COSMOS_KEY)

# Create the Data Source
data_source_name = "cosmosdb-datasource"
data_source_connection = SearchIndexerDataSourceConnection(
    name=data_source_name,
    type="cosmosdb",
    connection_string=f"AccountEndpoint={COSMOS_LINK};AccountKey={COSMOS_KEY};Database={COSMOS_DB_NAME};",
    container={"name": COSMOS_CONTAINER_NAME}
)

# Check if the data source already exists and create or update accordingly
try:
    existing_data_source = search_indexer_client.get_data_source_connection(data_source_name)
    search_indexer_client.create_or_update_data_source_connection(data_source_connection)
    print(f"Updated data source connection: {data_source_name}")
except Exception as e:
    search_indexer_client.create_data_source_connection(data_source_connection)
    print(f"Created new data source connection: {data_source_name}")

# Define field mappings
field_mappings = [
    FieldMapping(source_field_name="id", target_field_name="id"),
    FieldMapping(source_field_name="answer", target_field_name="answer"),
    FieldMapping(source_field_name="AnswerVector", target_field_name="AnswerVector"),
    FieldMapping(source_field_name="title", target_field_name="title"),
    FieldMapping(source_field_name="url", target_field_name="url"),
    FieldMapping(source_field_name="file_name", target_field_name="filename")
]

# Create the Indexer

indexer_name = "cosmosdb-indexer"
indexer = SearchIndexer(
    name=indexer_name,
    data_source_name=data_source_name,
    target_index_name=INDEX_NAME,
    field_mappings=field_mappings,
    schedule={"interval": "PT5M"}  # Every 5 minutes

)
search_indexer_client.create_indexer(indexer)

print("Search index, data source, and indexer created successfully.")
