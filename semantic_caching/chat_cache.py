from streamlit_chat import message
import streamlit as st
import sys
from dotenv import load_dotenv
from langchain.globals import set_llm_cache
from langchain_community.llms import OpenAI
from langchain.cache import RedisSemanticCache
from langchain_community.embeddings import OpenAIEmbeddings

load_dotenv()

# To make the caching really obvious, lets use a slower model.
llm = OpenAI(model_name="gpt-4")
set_llm_cache(
    RedisSemanticCache(redis_url="redis://localhost:6379", embedding=OpenAIEmbeddings())
)


def send_user_message(user_input):
    print(f"User input: {user_input}")
    response = llm(user_input)
    return response

global_user_context = {"content": []}

def chat():
    """
    This function facilitates an interactive chat session between a user and a 
    chatbot using Streamlit's interface. 
    The chatbot utilizes a given language model and corresponding embeddings. 
    The function provides controls to set the maximum number of tokens in responses, 
    randomness of responses, and to enable or disable embeddings mode. 
    The conversation's history is maintained in session variables, 
    allowing the model to generate contextually relevant responses.
    """
    print("chat")
    # st.write("Python executable:", sys.executable)
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""

        
    user_input = st.text_input("You:", key='input', value=st.session_state['user_input'])

    if user_input:
        # clear text input
        st.session_state.messages.append(
            {
                "message": user_input,
                "is_user": True,
            }
        )
        response = send_user_message(user_input)
        st.session_state.messages.append(
            {
                "message": response,
                "is_user": False,
            }
        )
        st.session_state['user_input'] = ""
    else:
        st.session_state['user_input'] = user_input

    for i in range(len(st.session_state['messages'])-1, -1, -1):
        message(st.session_state['messages'][i]["message"], is_user=st.session_state['messages'][i]["is_user"], key=str(i) + '_user')  




if __name__ == "__main__":
    chat()