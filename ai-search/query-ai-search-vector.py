import requests
from openai.embeddings_utils import get_embedding, cosine_similarity
import openai
import os
import json
from pprint import pprint

openai.api_type = "azure"
openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_base = os.environ['OPENAI_ENDPOINT']
openai.api_version = "2022-12-01"
print(os.environ['OPENAI_ENDPOINT'])


# send a query to the AI Search service
service_name = 'aisearch-aash'
index_name = 'faqdemo'
api_version = '2023-11-01'
api_key = os.environ['AI_SEARCH_KEY']

endpoint = f'https://{service_name}.search.windows.net/indexes/{index_name}/docs/search?api-version={api_version}'

question = "Can I skip the 30 days and just start with pay-as-you-go pricing?"

payload = json.dumps({
  "count": True,
  "select": "id, question, answer, Tags",
  "vectorQueries": [
    {
      "vector": get_embedding(question, engine="text-embedding-ada-002"),
      "k": 7,
      "fields": "AnswerVector",
      "kind": "vector",
      "exhaustive": True
    },
    {
      "vector": get_embedding(question, engine="text-embedding-ada-002"),
      "k": 7,
      "fields": "QuestionVector",
      "kind": "vector",
      "exhaustive": True
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'api-key': api_key
}

response = requests.request("POST", endpoint, headers=headers, data=payload)

pprint(response.json())
for r in response.json()["value"]:
    print(r["question"])
    print(r["answer"])
    print(r["Tags"])
    print(r["@search.score"])
    print(r["id"])
    print()