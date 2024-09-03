import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="ChatSnip", page_icon="📝")

st.title("ChatSnip - Chat Extractor")

# File upload and chat name input
uploaded_file = st.file_uploader("Upload a ChatGPT history/archive file:", type="html", key="file_uploader")
chat_name = st.text_input("Enter the chat name you want to snip out of the archive file:", key="chat_name")

# Extract Chat Button
if st.button("Extract Chat"):
    if uploaded_file is not None and chat_name:
        # Use quotes to handle multi-word chat names
        chat_name_quoted = f'"{chat_name}"'
        
        files = {'file': uploaded_file}
        data = {'chat_name': chat_name}
        response = requests.post("http://localhost:5000/extract_chat", files=files, data=data)
        
        if response.status_code == 200:
            chat_content = response.text
            st.success("Chat extracted successfully!")
            st.text_area("Chat Content", chat_content, height=400)
            st.download_button("Download Chat", data=chat_content, file_name=f"{chat_name}.txt", mime="text/plain")
        else:
            st.error("Chat not found or content could not be extracted.")
    else:
        st.error("Please upload a file and enter a chat name.")
