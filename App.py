import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Health Assistant", page_icon="⛑️")

# Read api from local file or cloud
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """
You are a health assistant expert Ai. only answer questions related to health, illness and medication
give proper advise beneficial to humans, if an image related to any illness is uploaded, please give requisite
advice else politely decline. At the end of every answer, give a note prompting to consult a medical doctor
for further clarifications. 
As a professional , you can identify illness and suggest prescription accordingly
"""

st.title("Health Assistant⛑️")

if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to your .env file or Streamlit secrets.")
    st.stop()

if "chat" not in st.session_state:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    st.session_state.chat = model.start_chat()

for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        for part in msg.parts:
            if hasattr(part, "text") and part.text:
                st.markdown(part.text)

image_file = st.file_uploader("📷 Upload a an image (optional)", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("Ask about your health and any illness...")

if user_input:
    message = [user_input]
    if image_file:
        message.append(Image.open(image_file))

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(message, stream=True)
        st.write_stream(chunk.text for chunk in response if chunk.text)

    st.rerun()
