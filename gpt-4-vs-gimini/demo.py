from streamlit_chat import message
import streamlit as st
from pprint import pprint
from glob import glob
import importlib
import json

def get_models():
    models = glob("models_halpers/*.py")
    models = [model.replace("models_halpers/", "").replace(".py", "") for model in models]
    return models

def get_roles_list():
    roles = {}
    roles_files = glob("roles/*.json")
    print(roles_files)
    for role_file in roles_files:
        print(f"role_file={role_file}")
        with open(role_file, 'r') as file:
            content = file.read()
            print("Content:", content)  # Check if there's any content
            print("Content type:", type(content))  # Check if there's any content
            roles[role_file] = json.loads(content)
        
    return roles

def get_role(role_name):
    file_name = 'roles/math_match.json'
    print(f"file_name={file_name}")
    with open(file_name, 'r') as file:
        content = file.read()
        print("Content:", content)  # Check if there's any content
        # role = json.loads(content)
    return None

def chat():
    print("chat")
    models = get_models()
    roles = get_roles_list()
    print(roles)
    # create combo box with the models
    st.sidebar.title("Models")
    modelA_selectbox = st.sidebar.selectbox("Select model A", models, 0)
    modelB_selectbox = st.sidebar.selectbox("Select model B", models, 1)
    judge_selectbox = st.sidebar.selectbox("Select Judge", models,2)
    roles_selectbox = st.sidebar.selectbox("Select role", list(roles.keys()), 1)

    role = roles[roles_selectbox]
    print(f"role={role}")
    print(f"modelA_selectbox={modelA_selectbox}")
    print(f"modelB_selectbox={modelB_selectbox}")
    # add image
    st.image('image.png', width=700)
    # st.write("Python executable:", sys.executable)
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    if 'modelA_role' not in st.session_state:
        st.session_state['modelA_role'] = ""    
    if 'modelB_role' not in st.session_state:
        st.session_state['modelB_role'] = ""  
    if 'judge_role' not in st.session_state:
        st.session_state['judge_role'] = ""

    # st.session_state['fight_started'] = False
    if 'fight_started' not in st.session_state:
        st.session_state['fight_started'] = False

    # st.session_state['message_index'] = 0
    if 'message_index' not in st.session_state:
        st.session_state['message_index'] = 0
    
    # prev_model = ""
    if 'prev_model' not in st.session_state:
        st.session_state['prev_model'] = ""
    if 'prev_msg' not in st.session_state:
        st.session_state['prev_msg'] = ""

    if 'start_response_modelA' not in st.session_state:
        st.session_state['start_response_modelA'] = ""

    if 'start_response_modelB' not in st.session_state:
        st.session_state['start_response_modelB'] = ""
    
    if 'session_initiated' not in st.session_state:
        st.session_state['session_initiated'] = False
  
    st.session_state['modelA_role'] = role["modelA_Role"]
    st.session_state['modelB_role'] = role["modelB_Role"]
    st.session_state['judge_role'] = role["judge_Role"]

    modelA_role = st.text_input(f"{modelA_selectbox} model A Role:", key='modelA_role', value=st.session_state['modelA_role'])
    modelB_role = st.text_input(f"{modelB_selectbox} model B Role:", key='modelB_role', value=st.session_state['modelB_role'])
    judge_role = st.text_input(f"{judge_selectbox} Judge Role:", key='judge_role', value=st.session_state['judge_role'])
    if modelA_role and modelB_role:
        st.button("Init", key='init')
    if st.session_state.get('init'):
        print("------init--------")
        if modelA_role:
            print(f"modelA_selectbox={modelA_selectbox}")
            # load model functions from models_halpers/{modelA_selectbox}.py using importlib
            init_role_modelA = getattr(importlib.import_module(f"models_halpers.{modelA_selectbox}"), "init_role")
            
            st.session_state['start_response_modelA'] , st.session_state['modelA-history'], time_modelA = init_role_modelA(modelA_role)
            st.success(f"{modelA_selectbox}  set")
            st.session_state['prev_msg'] = st.session_state['start_response_modelA']
        if modelB_role:
            print(f"modelB_selectbox={modelB_selectbox}")

            # load model functions from models_halpers/{modelB_selectbox}.py using importlib
            init_role_modelB = getattr(importlib.import_module(f"models_halpers.{modelB_selectbox}"), "init_role")
            
            st.session_state['start_response_modelB'], st.session_state['modelB-history'], time_modelB = init_role_modelB(modelB_role)
            st.success(f"{modelB_selectbox}  set")
        if judge_role:
            print(f"judge_role={judge_role}")
            # load model functions from models_halpers/{judge_selectbox}.py using importlib
            init_role_judge = getattr(importlib.import_module(f"models_halpers.{judge_selectbox}"), "init_role")
            
            st.session_state['start_response_judge'], st.session_state['judge-history'], time_judge = init_role_judge(judge_role)
            print("judge history init:")
            pprint(st.session_state['judge-history'])
            st.success(f"judge as {judge_selectbox}  set")
        st.session_state['messages'] = []
        st.session_state['fight_started'] = False
        st.session_state['message_index'] = 0
        st.session_state['prev_model'] = ""
        st.session_state['session_initiated'] = True

    
    
    if st.session_state.get('fight'):
        st.session_state['fight_started'] = True
        
        if st.session_state['prev_model'] == "modelB":
            print(f"modelA prev_msg={st.session_state['prev_msg']}")
            st.session_state['prev_model'] = "modelA"
            send_message_modelA = getattr(importlib.import_module(f"models_halpers.{modelA_selectbox}"), "send_message")
            response, st.session_state['modelA-history'], modelA_time = send_message_modelA(st.session_state['prev_msg'], st.session_state['modelA-history'])
            st.session_state['prev_msg'] = response
            st.session_state.messages.append(
                {
                    "message": response,
                    "is_user": False,
                }
            )
            print(f"model A response: {response}")
            judge_message = f"model A response: {response}"
            send_message_judge = getattr(importlib.import_module(f"models_halpers.{judge_selectbox}"), "send_message")
            judge_response, st.session_state['judge-history'], judge_time = send_message_judge(judge_message, st.session_state['judge-history'])
        else:
            print(f"modelB prev_msg={st.session_state['prev_msg']}")
            st.session_state['prev_model'] = "modelB"
            send_message_modelB = getattr(importlib.import_module(f"models_halpers.{modelB_selectbox}"), "send_message")
            response, st.session_state['modelB-history'], gpt_4_time = send_message_modelB(st.session_state['prev_msg'], st.session_state['modelB-history'])
            st.session_state['prev_msg'] = response
            st.session_state.messages.append(
                {
                    "message": response,
                    "is_user": True,
                }
            )
            print(f"model B response: {response}")
            judge_message = f"model B response: {response}"
            send_message_judge = getattr(importlib.import_module(f"models_halpers.{judge_selectbox}"), "send_message")
            print("judge history:")
            pprint(st.session_state['judge-history'])
            judge_response, st.session_state['judge-history'], judge_time = send_message_judge(judge_message, st.session_state['judge-history'])
        
        
            

        for i in range(len(st.session_state['messages'])):
            print("message:")
            print(st.session_state['messages'][i]["message"])
            if st.session_state['messages'][i]["is_user"]:
                st.write(f"model B({modelB_selectbox}):")
            else:
                st.write(f"model A({modelA_selectbox}):")
            message(st.session_state['messages'][i]["message"], is_user=st.session_state['messages'][i]["is_user"], key=str(i) + '_user')  
        st.write(f"judge: {judge_response}")

    if st.session_state['session_initiated']:
        st.button("Fight", key='fight')
    


if __name__ == "__main__":
    chat()