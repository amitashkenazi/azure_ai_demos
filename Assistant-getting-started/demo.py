from streamlit_chat import message as msg
import streamlit as st
from openai import AzureOpenAI
import dotenv
import os
import glob
import json
import time
from streamlit_chat import message
import uuid
from threads_handler import get_thread, get_thread_messages
from pprint import pprint

dotenv.load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-15-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_responses(function_name):
    print(f"get_responses function_name: {function_name}")
    responses = {}
    responses_files = glob.glob(f"responses/{function_name}/*.json")
    for file in responses_files:
        with open(file, "r") as f:
            data = f.read()
            responses[file] = data
    return responses

def wait_for_response(thread, run):
    start_time = time.time()

    status = run.status
    st.session_state["thread_status"][thread.id] = status

    while status not in ["completed", "cancelled", "expired", "failed", "requires_action"]:
        time.sleep(5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
        status = run.status
        print(f'Status: {status}')
        st.session_state["thread_status"][thread.id] = status
        
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    ) 

    print(f'Status: {status}')
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    print(messages.model_dump_json(indent=2))
    return messages, status, run

def create_assistant(instruction: str, model: str, name: str, functions: dict):
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-02-15-preview",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    functions_dict_to_api = []
    for function in functions:
        functions_dict_to_api.append(
            {
                "type": "function",
                "function": functions[function]
            }
        )

    # Create an assistant
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instruction,
        tools=[{"type": "code_interpreter"}] + functions_dict_to_api,
        model=model #You must replace this value with the deployment name for your model.
    )
    st.success(f"Assistant {name} created")
    return assistant

def get_roles():
    roles = {}
    roles_files = glob.glob("roles/*.txt")

def get_assistants():
    assistants_files = glob.glob("assistants_roles/*.txt")
    assistants = {}
    for file in assistants_files:
        with open(file, "r") as f:
            file_name_without_extension = os.path.splitext(file)[0]
            print(file_name_without_extension)
            data = f.read()
            assistants[file_name_without_extension] = data
    return assistants

def get_functions():
    functions_files = glob.glob("functions/*.json")
    functions = {}
    for file in functions_files:
        with open(file, "r") as f:
            file_name_without_extension = os.path.splitext(file)[0]
            print(file_name_without_extension)
            json_data = json.load(f)

            print(json_data)
            functions[file_name_without_extension] = json_data
    return functions


def refresh_to_thread(client, thread_id):
    # st.success(f"Thread: {thread_id} selected")
    thread = get_thread(client, thread_id)
    messages = get_thread_messages(client, thread_id)
    pprint(thread)
    print(f"Messages: {messages}")
    st.session_state.messages = []
    print(f"thread {thread_id} messages: ")
    for message in messages:
        print(f"Message: {message.content[0].text.value}")
        print(f"Role: {message.role}")
        st.session_state.messages.append(
            {
                "message": message.content[0].text.value,
                "is_user": message.role == "user",
            }
        )
        msg(message.content[0].text.value, message.role == "user", key=str(uuid.uuid4()))
    st.sidebar.text(f"Thread Status: {st.session_state['thread_status'][thread_id]}")

def chat():
    print("chat")
    # input text for the user to put the assistant role
    st.sidebar.header('Assisstant Demo')
    
        
    
    
    # st.text_area(f"Hello", key='modelA_role', value="Hello")
    if 'assistant' not in st.session_state:
        st.session_state['assistant'] = None
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'selected_functions' not in st.session_state:
        st.session_state['selected_functions'] = []
    if 'thread' not in st.session_state:
        st.session_state['thread'] = None
    if 'run' not in st.session_state:
        st.session_state['run'] = None
    if "threads" not in st.session_state:
        st.session_state["threads"] = []
    if "threads_buttons" not in st.session_state:
        st.session_state["threads_buttons"] = {}
    if "waiting_for_response" not in st.session_state:
        st.session_state["waiting_for_response"] = False
    if 'session' not in st.session_state:
        st.session_state['session'] = {"session": str(uuid.uuid4())}  
        # create a session json file in sessions/<>.json
        with open(f"sessions/{st.session_state['session']['session']}.json", "w") as f:
            f.write(json.dumps(st.session_state["session"]))
    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = None

    if "tool_calls" not in st.session_state:  
        st.session_state["tool_calls"] = None
    if "thread_status" not in st.session_state:
        st.session_state["thread_status"] = {}

    st.session_state["waiting_for_action"] = False

    functions = get_functions()
    assistants = get_assistants()
    print(assistants)
    selected_functions_dict = {}
    
    # create a streamlit combo box to select the assistant. single selection
    st.header("Create an assistant")
    selected_assistant = st.selectbox("Select assistant", list(assistants.keys()))
    selected_functions = st.multiselect("Select functions", list(functions.keys()))
    if selected_functions:
        st.session_state["selected_functions"] = selected_functions
    
        # create a new dict with only the selected functions
        for function in selected_functions:
            selected_functions_dict[function] = functions[function]

    if selected_assistant:
        st.text_area(f"Assistant: {selected_assistant}", value=assistants[selected_assistant])
        create_assistant_btn = st.button("Create assistant")
        if create_assistant_btn:
            st.session_state["assistant"] = create_assistant(assistants[selected_assistant], "gpt-4", selected_assistant, selected_functions_dict)
            # st.success(f"Assistant {selected_assistant} created functions: {st.session_state['selected_functions']}")
    
    if st.session_state['assistant']:
        st.sidebar.text(f"Assistant: {st.session_state['assistant'].id}")
        st.sidebar.text(f"Assistant: {st.session_state['assistant']}")
        st.header("Threads")
        create_thread = st.button("Create thread")
        if create_thread:
            print("create thread")
            st.session_state["thread"] = client.beta.threads.create()
            st.session_state["thread_status"][st.session_state["thread"].id] = "created"
            if "threads" not in st.session_state["session"]:
                st.session_state["session"]["threads"] = []
            st.session_state["session"]["threads"].append(st.session_state["thread"].id)
            st.session_state["threads"].append(st.session_state["thread"].id)
            with open(f"sessions/{st.session_state['session']['session']}.json", "w") as f:
                f.write(json.dumps(st.session_state["session"]))
            # refresh_to_thread(client, st.session_state["thread"].id)
            st.session_state["selected_thread"] = st.session_state["thread"].id
            
            
            
        if len(st.session_state["threads"]) > 0:
            selected_thread = st.sidebar.selectbox("Select thread", list(st.session_state["threads"]), index=len(st.session_state["threads"]) - 1)
            if selected_thread:
                print("---------------------------")
                st.session_state["selected_thread"] = selected_thread
                st.session_state["thread_id"] = selected_thread
                st.session_state["thread"] = get_thread(client, selected_thread)
                # refresh_to_thread(client, selected_thread)
                
                
                    
            
    if st.session_state['assistant'] is not None:
        
        if not st.session_state["waiting_for_response"]:
            submit = False
            if st.session_state["thread"] is not None:
                user_input=st.text_input("You:",key='input')
                submit = st.button("Submit")
            if submit:
                st.success(f"You said: {user_input}")
                # st.session_state.messages.append(
                #     {
                #         "message": user_input,
                #         "is_user": True,
                #     }
                # ) 
                # # Add a new user question to the thread
                message = client.beta.threads.messages.create(
                    thread_id=st.session_state["thread"].id,
                    role="user",
                    content=user_input
                )
                run = client.beta.threads.runs.create(
                    thread_id=st.session_state["thread"].id,
                    assistant_id=st.session_state["assistant"].id,
                    #instructions="New instructions" #You can optionally provide new instructions  but these will override the default instructions
                    )

                messages, status, run = wait_for_response(st.session_state["thread"], run)

                if status == "requires_action":
                    # st.success("Requires action")
                    # print("Requires action")
                    st.session_state["tool_calls"] = json.loads(run.required_action.model_dump_json(indent=2))['submit_tool_outputs']['tool_calls']
                    st.session_state["waiting_for_response"] = True
                    st.session_state["run"] = run
                    st.session_state["thread_status"][st.session_state["thread"].id] = status
                        
            
        if st.session_state["waiting_for_response"]:
            st.success("Waiting for a response")
            for tool_call in st.session_state["tool_calls"]:
                st.text("waiting for a response for the following function:")
                st.text(f"function name: {tool_call['function']['name']}")
                st.text(f"function name: {tool_call['function']['arguments']}")        
                st.text(f"tool call: {tool_call}")   
                print(f"tool call: {tool_call}")     
                
                st.session_state["waiting_for_response"] = True
                    
                response_combo = st.selectbox("Select response", get_responses(tool_call['function']['name']), key="response")
                
                
                response = ""
                try:
                    file_name = response_combo
                    with open(file_name) as f:
                        response = f.read()
                        st.text_area("Response", value=response)
                except:
                    print(f"File {response_combo} not found")
                    response = st.text_area("Response")
                submit_response = st.button("Submit response")
                
                if submit_response:
                    # st.success(f"Response: {response}")
                    # read the response and present it in text_area
                    try:
                        file_name = response_combo
                        with open(file_name) as f:
                            response = f.read()
                            st.text_area("Response", value=response)
                    except:
                        print(f"File {response_combo} not found")
                    if response:
                        st.success(f"Response: {response}")
                        st.session_state["waiting_for_response"] = False
                        run = st.session_state["run"]
                        run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id=st.session_state["thread"].id,
                            run_id=run.id,
                            tool_outputs=[
                                {
                                    "tool_call_id": tool_call["id"],
                                    "output": response,
                                }
                                ]
                            )
                        messages, status, run = wait_for_response(st.session_state["thread"], run)
                        print(f"Status: {status}")
                        print(f'messages: {messages}')
                        st.session_state["waiting_for_response"] = False
                        st.button("Refresh")
                        
                
                    st.session_state["tool_calls"] = None
            
        # else:
        #     st.success("Not waiting for a response")
    if st.session_state["thread"] is not None:        
        refresh_to_thread(client, selected_thread)


if __name__ == "__main__":
    chat()

