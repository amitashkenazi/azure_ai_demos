import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
service_name = os.environ['AI_SEARCH_SERVICE']


name = os.environ['AI_SEARCH_INDEX_NAME']
url = f"https://{service_name}.search.windows.net/indexes/{name}?api-version=2023-11-01"
payload = json.dumps({
  "name": name,
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "searchable": False,
      "filterable": True,
      "retrievable": True,
      "sortable": False,
      "facetable": False,
      "key": True,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": None,
      "fields": []
    },
    {
      "name": "answer",
      "type": "Edm.String",
      "searchable": True,
      "filterable": True,
      "retrievable": True,
      "sortable": True,
      "facetable": False,
      "key": False,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": "en.microsoft",
      "fields": []
    },
    {
      "name": "AnswerVector",
      "type": "Collection(Edm.Single)",
      "searchable": True,
      "retrievable": True,
      "dimensions": 1536,
      "vectorSearchProfile": "my-vector-profile"
    },
    {
      "name": "filename",
      "type": "Edm.String",
      "searchable": True,
      "filterable": True,
      "retrievable": True,
      "sortable": True,
      "facetable": False,
      "key": False,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": None,
      "fields": []
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": True,
      "filterable": True,
      "retrievable": True,
      "sortable": True,
      "facetable": False,
      "key": False,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": None,
      "fields": []
    },
    {
      "name": "url",
      "type": "Edm.String",
      "searchable": True,
      "filterable": True,
      "retrievable": True,
      "sortable": True,
      "facetable": False,
      "key": False,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": None,
      "fields": []
    },
    {
      "name": "Tags",
      "type": "Collection(Edm.String)",
      "searchable": True,
      "filterable": True,
      "retrievable": True,
      "sortable": False,
      "facetable": True,
      "key": False,
      "indexAnalyzer": None,
      "searchAnalyzer": None,
      "analyzer": None,
      "fields": []
    }
],
  "corsOptions": {
    "allowedOrigins": [
      "*"
    ],
    "maxAgeInSeconds": 60
  },
  "vectorSearch": {
    "algorithms": [
      {
        "name": "my-hnsw-config",
        "kind": "hnsw",
        "hnswParameters": {
          "m": 4,
          "efConstruction": 400,
          "efSearch": 500,
          "metric": "cosine"
        }
      },
      {
        "name": "my-eknn-config",
        "kind": "exhaustiveKnn",
        "exhaustiveKnnParameters": {
          "metric": "cosine"
        }
      }
    ],
    "profiles": [
      {
        "name": "my-vector-profile",
        "algorithm": "my-hnsw-config"
      }
    ]
  },
  "semantic": {
    "configurations": [
      {
        "name": "my-semantic-config",
        "prioritizedFields": {
        #   "titleField": {
        #     "fieldName": "HotelName"
        #   },
            
          "prioritizedContentFields": [
            {
              "fieldName": "answer"
            }
          ],
          "prioritizedKeywordsFields": [
            {
              "fieldName": "Tags"
            }
          ]
        }
      }
    ]
  }
})
headers = {
  'Content-Type': 'application/json',
  'api-key': os.environ['AI_SEARCH_KEY']
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.status_code)
print(response.text)
