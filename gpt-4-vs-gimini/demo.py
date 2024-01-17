from streamlit_chat import message
import streamlit as st
from gpt_4 import send_message_gpt_4, init_role as init_role_gpt_4
from gemini import send_message_gemini, init_role as init_role_gemini
from pprint import pprint



def chat():
    print("chat")
    # add image
    st.image('image.png', width=700)
    # st.write("Python executable:", sys.executable)
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    if 'gimini_role' not in st.session_state:
        st.session_state['gimini_role'] = ""    
    if 'gpt_4_role' not in st.session_state:
        st.session_state['gpt_4_role'] = ""  

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

    if 'start_response_gemini' not in st.session_state:
        st.session_state['start_response_gemini'] = ""

    if 'start_response_gpt_4' not in st.session_state:
        st.session_state['start_response_gpt_4'] = ""
    
    if 'session_initiated' not in st.session_state:
        st.session_state['session_initiated'] = False
  
    
    gimini_role = st.text_input("Gemini Role:", key='gimini_role', value=st.session_state['gimini_role'])
    gpt_4_role = st.text_input("GPT-4 Role:", key='gpt_4_role', value=st.session_state['gpt_4_role'])
    selectbox = st.selectbox("Starting model", ["gpt-4", "gemini"],0)
    if gimini_role and gpt_4_role:
        st.button("Init", key='init')
    if st.session_state.get('init'):
        print("------init--------")
        if gimini_role:
            st.session_state['start_response_gemini'] , st.session_state['gemini-history'], time_gemini = init_role_gemini(gimini_role)
            st.success("Gemini role set")
        if gpt_4_role:
            st.session_state['start_response_gpt_4'], st.session_state['gpt-4-history'] = init_role_gpt_4(gpt_4_role)
            st.success("GPT-4 role set")
        st.session_state['messages'] = []
        st.session_state['fight_started'] = False
        st.session_state['message_index'] = 0
        st.session_state['prev_model'] = ""
        st.session_state['prev_msg'] = ""
        st.session_state['session_initiated'] = True

    
    
    if st.session_state.get('fight'):
        st.session_state['fight_started'] = True
        

        # st.session_state.messages.append(
        #     {
        #         "message": response,
        #         "is_user": False,
        #     }
        # )
        # st.session_state['gimini_role'] = ""
        
        if st.session_state['message_index'] == 0:
            st.session_state['message_index'] += 1
            print(selectbox)
            if selectbox == "gpt-4":
                st.session_state['prev_model'] = "gpt-4"
                st.session_state.messages.append(
                    {
                        "message": st.session_state['start_response_gemini'],
                        "is_user": False,
                    }
                )
                response, st.session_state['gpt-4-history'], gpt_4_time = send_message_gpt_4(st.session_state['start_response_gemini'] , st.session_state['gpt-4-history'])
                st.session_state['prev_msg'] = response
                st.session_state.messages.append(
                    {
                        "message": response,
                        "is_user": True,
                    }
                )
            else:
                st.session_state['prev_model'] = "gemini"
                st.session_state.messages.append(
                    {
                        "message": st.session_state['start_response_gpt_4'],
                        "is_user": True,
                    }
                )
                response, st.session_state['gemini-history'], gemini_time = send_message_gemini(st.session_state['start_response_gpt_4'], st.session_state['gemini-history'])
                st.session_state['prev_msg'] = response
                st.session_state.messages.append(
                    {
                        "message": response,
                        "is_user": False,
                    }
                )
        else:
            if st.session_state['prev_model'] == "gpt-4":
                st.session_state['prev_model'] = "gemini"
                response, st.session_state['gemini-history'], gemini_time = send_message_gemini(st.session_state['prev_msg'], st.session_state['gemini-history'])
                st.session_state['prev_msg'] = response
                st.session_state.messages.append(
                    {
                        "message": response,
                        "is_user": False,
                    }
                )
            else:
                st.session_state['prev_model'] = "gpt-4"
                response, st.session_state['gpt-4-history'], gpt_4_time = send_message_gpt_4(st.session_state['prev_msg'], st.session_state['gpt-4-history'])
                st.session_state['prev_msg'] = response
                st.session_state.messages.append(
                    {
                        "message": response,
                        "is_user": True,
                    }
                )

        for i in range(len(st.session_state['messages'])):
            print("message:")
            print(st.session_state['messages'][i]["message"])
            message(st.session_state['messages'][i]["message"], is_user=st.session_state['messages'][i]["is_user"], key=str(i) + '_user')  

    if st.session_state['session_initiated']:
        st.button("Fight", key='fight')
    


if __name__ == "__main__":
    chat()