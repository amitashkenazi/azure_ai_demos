import requests
import json
from cosmosdb_handler import get, check_container, check_database
from pprint import pprint
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = AzureOpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    azure_endpoint=os.environ['OPENAI_ENDPOINT'],
    api_version="2024-02-01"
)
api_version = '2020-06-30'

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=text,
    model=model)
    return response.data[0].embedding

print(os.environ['OPENAI_ENDPOINT'])


service_name = os.environ['AI_SEARCH_SERVICE']
index_name = os.environ['AI_SEARCH_INDEX_NAME'] 
print(f"Index name: {index_name}")

endpoint = f'https://{service_name}.search.windows.net/indexes/{index_name}/docs/index?api-version={api_version}'

headers = {
    'Content-Type': 'application/json',
    'api-key': os.environ['AI_SEARCH_KEY']
}

if __name__ == "__main__":
    chunks = []
    print(check_database('faqdemo'))
    print(check_container('faqdemo'))
    docs = get()
    for d in docs:
        pprint(d)
        embedding_q = get_embedding(
            d["question"],
            model="text-embedding-ada-002"
        )
        print("embedding_q")
        embedding_a = get_embedding(
            d["answer"],
            model="text-embedding-ada-002"
        )

        chunk = {
            "id": d["id"],
            "answer": d["answer"],
            "url": d["url"],
            "title": d["title"],
            "filename": d["file_name"],
            "AnswerVector": embedding_a,
            "Tags": ["FAQ", "Azure"]
        }
        chunks.append(chunk)

    batch = {
        "value": chunks
    }

    # Convert the batch to a JSON string
    payload = json.dumps(batch)
    print(f"sending to {endpoint}")
    response = requests.post(endpoint, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)