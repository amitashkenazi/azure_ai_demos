import openai, os, requests

# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version

# Azure OpenAI setup
 # Add your endpoint here
 # Add your OpenAI API key here
deployment_id = "gpt-4" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://ai-search-aash-demo.search.windows.net"; # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY"); # Add your Azure AI Search admin key here
search_index_name = "faqdemo-extended"; # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    # TODO: The 'openai.requestssession' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(requestssession=session)'
    # openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    dataSources=[  # camelCase is intentional, as this is the format the API expects
      {
  "type": "AzureCognitiveSearch",
  "parameters": {
    "endpoint": "$search_endpoint",
    "indexName": "$search_index",
    "semanticConfiguration": None,
    "queryType": "vectorSimpleHybrid",
    "fieldsMapping": {
      "contentFieldsSeparator": "\n",
      "contentFields": [
        "question",
        "answer"
      ],
      "filepathField": "filename",
      "titleField": "title",
      "urlField": "url",
      "vectorFields": [
        "QuestionVector",
        "AnswerVector"
      ]
    },
    "inScope": True,
    "roleInformation": "You are an AI assistant that helps people find information.",
    "filter": None,
    "strictness": 3,
    "topNDocuments": 5,
    "key": "$search_key",
    "embeddingDeploymentName": "text-embedding-ada-002"
  }
}
    ],
    temperature=0,
    top_p=1,
    max_tokens=800,
    stream=True

)
print(completion)