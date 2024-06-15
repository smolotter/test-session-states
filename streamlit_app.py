import streamlit as st
import os

# Upload section
uploaded_file = st.file_uploader("Choose a ZIP file to upload", type="zip")

# Download section
download_button = st.button("Download test.zip")

# Logic for saving and downloading
if uploaded_file is not None:
    with open(os.path.join("test.zip"), "wb") as f:
        f.write(uploaded_file.read())
    st.success("File uploaded as test.zip")

if download_button:
    # Check if file exists before downloading
    if os.path.exists("test.zip"):
        with open("test.zip", "rb") as f:
            st.download_button(
                label="Download test.zip",
                data=f,
                file_name="test.zip",
                mime="application/zip"
            )
    else:
        st.warning("No file uploaded yet. Upload a ZIP file first.")

