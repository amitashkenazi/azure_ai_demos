import openai
import os
from dotenv import load_dotenv
import time
load_dotenv()

openai.api_type = "azure"
openai.api_base = os.environ['OPENAI_ENDPOINT']
openai.api_version = "2023-07-01-preview"
openai.api_key = os.environ['OPENAI_API_KEY']

def init_role(role):
    global history
    history = [{"role": "system", "content": role}]
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages = history,
        temperature=0.5,
    )
    
    return response["choices"][0]["message"], history


def send_message_gpt_4(message, history):
    print(send_message_gpt_4)
    history.append({"role": "user", "content": message})
    print(history)
    start_time = int(time.time()*1000)
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages = history,
        temperature=0.5,
        # max_tokens=500,
    )
    end_time = int(time.time()*1000)
    history.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
    print(response["choices"][0]["message"]["content"])
    return (response["choices"][0]["message"]["content"], history, end_time-start_time)
