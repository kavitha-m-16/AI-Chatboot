import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

#Load Environment Variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client=Groq(api_key=api_key)

#Streamlit page Configuration
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="",
    layout="wide"
)
#Title
st.title("Groq AI Chatbot")
st.write("Powered by Groq Llama Models")

#Sidebar
st.sidebar.title("Settings")
model = st.sidebar.selectbox(
    "Choose Model",
     [
         "llama-3.3-70b-versatile",
         "llama-3.1-8b-instant"
     ]
)
temperature = st.sidebar.slider(
    "Temperature",
    0.0,
    1.0,
    0.7
)
max_tokens = st.sidebar.slider(
    "Max Tokens",
    100,
    2048,
    1024
)
if st.sidebar.button("Clear Chat"):
    st.session_state.messages=[]
if "messages" not in st.session_state:
    st.session_state.messages = []

#Display chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#User Input
prompt = st.chat_input("Ask Anything....")
if prompt:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistent"):
        with st.spinner("Thinking...."):
            response = client.chat.completions.create(
                model = model,
                messages = st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
        reply = response.choices[0].message.content
        st.markdown(reply)
    st.session_state.messages.append(
        {
            "role":"assistent",
            "content":reply
        }
    )



