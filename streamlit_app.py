import streamlit as st


import os
import time

st.write ("init")

st.write(os.listdir("/tmp"))

uploaded_file = st.file_uploader("Upload HTML File")

if uploaded_file is not None:
  # Save the uploaded file to /tmp/banana.html
  with open("/tmp/banana.html", "wb") as f:
    f.write(uploaded_file.read())
  st.success("File uploaded and saved to /tmp/banana.html")

try:
    with open("/tmp/banana.html", "rb") as f:
        data = f.read()
        st.download_button(label="Download", data=data, file_name="banana.html")
    st.write("file is found")
except:
    st.write("no file found")


st.write(os.listdir("/tmp"))