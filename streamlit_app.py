import streamlit as st
import os
import time
import tempfile
import zipfile
import uuid




st.write ("init")

# Create a UUID
session_uuid = str(uuid.uuid4())
st.write(session_uuid)

st.write("listdir /tmp")
st.write(os.listdir("/tmp"))



# if uploaded_file is not None:
#   # Save the uploaded file to /tmp/banana.html
#   with open("/tmp/banana.html", "wb") as f:
#     f.write(uploaded_file.read())
#   st.success("File uploaded and saved to /tmp/banana.html")

# try:
#     with open("/tmp/banana.html", "rb") as f:
#         data = f.read()
#         st.download_button(label="Download", data=data, file_name="banana.html")
#     st.write("file is found")
# except:
#     st.write("no file found")


# st.write(os.listdir("/tmp"))



import tempfile
import os

with tempfile.TemporaryDirectory() as temp_dir:
    # Create a temporary file inside the directory
    filename = "temp_file.txt"
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, 'w') as f:
        f.write("This is some data in the temporary file")

    # Print the contents of the temporary file (outside the with block for file access)
    print(f"Contents of {filename} in temporary directory:")
    with open(filepath, 'r') as f:
        contents = f.read()
        print(contents)



with tempfile.TemporaryDirectory() as temp_dir:
    uploaded_file = st.file_uploader("Upload File")

    with zipfile.ZipFile(BytesIO(temp_dir), 'r') as zip_ref:
        zip_ref.extractall(folder_name) # Note that zip file needs to be extracted to local disk so that the css/images can work.



    file_name = zip_obj.name
    folder_name = "/tmp/" + file_name + "_" + session_uuid

    zip_data = zip_obj.read()

    # Unzip the file
                
        st.write(f"...contents of {folder_name} is {zip_ref.namelist()}")
        
    # Get list of files in the directory (this only looks at the parent directory, not the subdirectories.)
    files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]

    for file in files:
        if file.endswith(".html"):  # Check if filename ends with ".html"
            st.write(f"...... processing {file}")
            pdf_path = html_to_pdf(folder_name + "/" + file)
            st.write(f"...... pdf path is {pdf_path}")
            pdf_files[comp_name + "_" + file.replace(".html",".pdf")] = pdf_path