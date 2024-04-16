import os
from openai import AzureOpenAI
import json
from pprint import pprint

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="2023-12-01-preview"
)
# open data/faqs.csv file and get all the questions and answers
import pandas as pd
df = pd.read_csv("data/faqs.csv")
prompt = ""
for i, row in df.iterrows():
  prompt += f"Q: {row['question']}\nA: {row['answer']}\n"
print(prompt)
# Call the chat endpoint with the prompt

response = client.chat.completions.create(
  model="gpt-4-turbo", # Model = should match the deployment name you chose for your 1106-preview model deployment
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON. write a list of 10 possible questions and aswers according to the data provided by the user"},
    {"role": "user", "content": prompt}
  ]
)


res = response.choices[0].message.content
json_res = json.loads(res)
pprint(json_res)