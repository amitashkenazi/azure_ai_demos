from openai import AzureOpenAI
import os
import json
print(os.environ['OPENAI_ENDPOINT'])

client = AzureOpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        azure_endpoint=os.environ['OPENAI_ENDPOINT'],
        api_version="2024-02-01"
    )
    
def analyze_image(image_url):
    response = client.chat.completions.create(
        model="gpo-4o-global",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """You are an assistant helping to extract metadata from an images in order to index them in a search service.
             respond in the following json format:
                {
                    "image_description": <detailed description to be indexed>,
                    "image_title": <title of the image to be indexed>,
                }
             """},
            { "role": "user", "content": [
                 { 
                "type": "text", 
                "text": """
                this is an image that should deonstrate what services are available under the azure free trial. 
                I want to index this image so Ill be able to show it when neccassary during conversation with a user. 
                write detailed information and metadata about the image. This will be indexed and stored in a search service and will be used to decide when to show the image to a user.
                give high level description as well as detailed description of the image.
                
                """
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]}
        ],
        max_tokens=1000

        

    )
    print(response.choices[0].message.content)
    json_res = response.choices[0].message.content
    start = json_res.find("{")
    end = json_res.rfind("}")
    return json.loads(json_res[start:end+1])

if __name__ == "__main__":
    res = analyze_image("https://new2cloud.de/wp-content/uploads/2021/04/CreateAzureFreeAccount-1-1536x879.png")
    print(json.loads(res))