from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream= True)
    return response

st.set_page_config(page_title='ChatterMate')
st.header('ChatterMate using Gemini LLM')

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# if 'temp_input' not in st.session_state:
#     st.session_state['temp_input'] = ''

input = st.text_input('You: ', key='input')
submit = st.button('Ask')

if submit or input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(('You', input))
    st.subheader('Response:')
    full_response = ""
    for chunk in response:
        st.write(chunk.text)
        full_response += chunk.text
    st.session_state['chat_history'].append(('Bot', full_response))
    
    # st.session_state['temp_input'] = ''

st.subheader('Chat History:')

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")