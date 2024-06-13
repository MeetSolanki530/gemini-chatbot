import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

#load environment variable

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#Configure strealit page settings

st.set_page_config(
    page_title="Chatbot With GOOGLE GEMINI",
    page_icon= ":brain:", #favicon emoji
    layout= "centered", #page layout screen
)

#setup gemini pro ai model

gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

#function to translate rules between Gemini-pro and streamlit terminology

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    

#Initialize chat session in Streamlit if not already present

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

#Display the chatbot's title on the page

st.title("Gemini Chatbot")

#Display the chat history

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)
    
#input field for users message

user_prompt = st.chat_input("Ask Gemini Model...")


if user_prompt:
    with st.spinner("Thinking..."):
        #add users message to chat and display it

        st.chat_message("user").markdown(user_prompt)

        #send users message in gemini-pro and get the responce

        gemini_responce = st.session_state.chat_session.send_message(user_prompt)

        #Display gemini's response

        with st.chat_message("assistant"):
            st.markdown(gemini_responce.text)


