from openai import AzureOpenAI
from pprint import pprint
import os


containter_app_url = os.getenv("CONTAINER_APP_URL")
containter_app_key = os.getenv("CONTAINER_APP_KEY")

client = AzureOpenAI(
    azure_endpoint=containter_app_url,
    api_key=containter_app_key,
    api_version="2023-12-01-preview"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the first letter of the alphabet?"}
    ]
)
pprint(response)