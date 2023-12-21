import requests
import json
from cosmosdb_handler import store, get, delete_item, delete_all_matches, update_item
from pprint import pprint
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import os

openai.api_type = "azure"
openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_base = os.environ['OPENAI_ENDPOINT']
openai.api_version = "2022-12-01"
print(os.environ['OPENAI_ENDPOINT'])


service_name = os.environ['AI_SEARCH_SERVICE']
index_name = 'faqdemo'
api_version = '2020-06-30'
endpoint = f'https://{service_name}.search.windows.net/indexes/{index_name}/docs/index?api-version={api_version}'

headers = {
    'Content-Type': 'application/json',
    'api-key': os.environ['AI_SEARCH_KEY']
}

if __name__ == "__main__":
    chunks = []

    docs = get()
    for d in docs:
        print(d["id"])
        print(d["question"])
        print(d["answer"])
        embedding_q = get_embedding(
            d["question"],
            engine="text-embedding-ada-002"
        )
        print("embedding_q")
        embedding_a = get_embedding(
            d["answer"],
            engine="text-embedding-ada-002"
        )

        chunk = {
            "id": d["id"],
            "question": d["question"],
            "answer": d["answer"],
            "QuestionVector": embedding_q,
            "AnswerVector": embedding_a,
            "Tags": ["FAQ", "Azure"]
        }
        chunks.append(chunk)

    batch = {
        "value": chunks
    }

    # Convert the batch to a JSON string
    payload = json.dumps(batch)
    print("sending...")
    response = requests.post(endpoint, headers=headers, data=payload)
    print(response.status_code)
    print(response.text)