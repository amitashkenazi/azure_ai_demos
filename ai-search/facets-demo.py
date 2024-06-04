import requests
import json
import os
from pprint import pprint
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    azure_endpoint=os.environ['OPENAI_ENDPOINT'],
    api_version="2022-12-01"
)

# Function to get embedding for a text
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

# Set up environment variables and endpoint
service_name = os.environ['AI_SEARCH_SERVICE']
index_name = os.environ['AI_SEARCH_INDEX_NAME']  # 'faqdemo-extended'
api_version = '2023-11-01'
api_key = os.environ['AI_SEARCH_KEY']
endpoint = f'https://{service_name}.search.windows.net/indexes/{index_name}/docs/search?api-version={api_version}'

# Define the search query and facet request
question = "Can I skip the 30 days and just start with pay-as-you-go pricing?"
payload = json.dumps({
    "count": True,
    "search": question,
    "select": "id, question, answer, Tags",
    "facets": ["Tags"],
    "top": 7,
    "vectorQueries": [
        {
            "vector": get_embedding(question, model="text-embedding-ada-002"),
            "k": 3,
            "fields": "AnswerVector",
            "kind": "vector",
            "exhaustive": True
        }
    ]
})
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}

# Perform the search query
response = requests.post(endpoint, headers=headers, data=payload)
response_data = response.json()

# Print the response for debugging
pprint(response_data)

# Print the search results
print("Search Results:")
for r in response_data.get("value", []):
    print(f"Question: {r['question']}")
    print(f"Answer: {r['answer']}")
    print(f"Tags: {r.get('Tags', [])}")
    print(f"Search Score: {r['@search.score']}")
    print(f"ID: {r['id']}")
    print()

# Print the facets
print("Facets:")
for facet in response_data.get("facets", {}).get("Tags", []):
    print(f"Tag: {facet['value']} (Count: {facet['count']})")
