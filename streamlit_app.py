import streamlit as st


import os
import time

def delete_old_files(directory):
  """
  Deletes files older than 5 minutes from the specified directory.

  Args:
    directory: The path to the directory to scan.
  """
  # Get current time in seconds
  current_time = time.time()
  # Convert 1 minutes to seconds
  five_minutes = 1 * 60

  for root, _, files in os.walk(directory):
    for filename in files:
      # Get the full path of the file
      file_path = os.path.join(root, filename)
      # Get the last modification time of the file
      last_modified = os.path.getmtime(file_path)
      
      # Check if the file is older than 5 minutes
      if current_time - last_modified > five_minutes:
        # Delete the file
        os.remove(file_path)
        print(f"Deleted: {file_path}")

# Replace 'path/to/your/directory' with the actual directory path
directory = 'tmp'
delete_old_files(directory)
print("Finished cleaning directory.")





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


