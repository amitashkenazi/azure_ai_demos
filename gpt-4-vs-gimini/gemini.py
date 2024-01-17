import pathlib
import textwrap
import time
import google.generativeai as genai


from IPython.display import display
from IPython.display import Markdown

GOOGLE_API_KEY="AIzaSyDdh7-zr3e9vCWGtx6GzFIKGHZHhwA0Vk8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def init_role(role):
    print("init_gemini")
    history = []
    chat = model.start_chat(history=history)
    role_message = "in the following session your role is: " + role + "in the response for this message just return a single sentence of what is the first sentence that you will say according to the role"
    return send_message_gemini(role_message, chat.history)

def send_message_gemini(message, history):
    chat = model.start_chat(history=history)
    start_time = int(time.time()*1000)
    response = chat.send_message(message)
    end_time = int(time.time()*1000)
    history = chat.history
    return(response.text, history, end_time-start_time)


if __name__ == "__main__":

    print("------1-------")
    print(send_user_message_gemini("How are you?"))
    print("history:")
    print(history)
    print()
    print("------2-------")
    print(send_user_message_gemini("I want to purchase an iphone 14, how much it costs."))
    print("history:")
    print(history)