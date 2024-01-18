import openai
import os
# from dotenv import load_dotenv
import time
# load_dotenv()
import cohere 

co = cohere.Client('YlJAKrY28IMwie1eyZFcBgTbS8NhfWlerUX3KJy7')

def init_role(role):    
    role_message = "in the following session your role is: " + role + "in the response for this message just return a single sentence of what is the first sentence that you will say according to the role"
    response = co.chat( 
        model='command',
        message=role_message,
        temperature=0.3,
        chat_history=[],
        prompt_truncation='AUTO',
        stream=False,
        citation_quality='accurate',
        connectors=[],
        documents=[]
    ) 
    print(response)
    chat_history=[{"role": "User", "message": role_message}, {"role": "Chatbot", "message": response.text}]
    return (response.text, chat_history, None)


def send_message(message, history):
    start_time = int(time.time()*1000)
    response = co.chat( 
        model='command',
        message=message,
        temperature=0.3,
        chat_history=[],
        prompt_truncation='AUTO',
        stream=False,
        citation_quality='accurate',
        connectors=[],
        documents=[]
    )
    end_time = int(time.time()*1000)
    history.append({"role": "user", "content": message})
    history.append({"role": "Chatbot", "content": response.text})
    return (response.text, history, end_time-start_time)


if __name__ == "__main__":
    r,h,t = init_role("hello")