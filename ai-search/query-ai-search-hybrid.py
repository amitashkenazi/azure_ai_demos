import requests
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(api_key=os.environ['OPENAI_API_KEY'],
azure_endpoint=os.environ['OPENAI_ENDPOINT'],
api_version="2022-12-01")
import os
import json
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
# Set up OpenAI API
print(os.environ['OPENAI_ENDPOINT'])

# Get embedding for the question
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=text,
    model=model)
    return response.data[0].embedding

# Send a query to the AI Search service
service_name = os.environ['AI_SEARCH_SERVICE']
index_name = 'faqdemo'
api_version = '2023-11-01'
api_key = os.environ['AI_SEARCH_KEY']

endpoint = f'https://{service_name}.search.windows.net/indexes/{index_name}/docs/search?api-version={api_version}'

question = "Can I skip the 30 days and just start with pay-as-you-go pricing?"
payload = json.dumps({
  "count": True,
  "search": question,
  "select": "id, question, answer, Tags",
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

response = requests.request("POST", endpoint, headers=headers, data=payload)

pprint(response.json())
for r in response.json()["value"]:
    print(r["question"])
    print(r["answer"])
    print(r["Tags"])
    print(r["@search.score"])
    print(r["id"])
    print()
    