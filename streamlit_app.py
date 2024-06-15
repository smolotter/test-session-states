import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os
from collections import OrderedDict
from PyPDF2 import PdfWriter
import time
import uuid



st.title("ZIP to PDF Converter")

# Create a UUID
session_uuid = str(uuid.uuid4())


# Accept 4 zip files
zip_1 = st.file_uploader("Upload Covernote (if any)", type="zip")
zip_2 = st.file_uploader("Upload Main Product", type="zip")
zip_3 = st.file_uploader("Upload Annex (if any)", type="zip")
zip_4 = st.file_uploader("Upload Distriubtion List", type="zip")

# Define function to convert html to pdf
def html_to_pdf(html_file_path):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()

    command = [
        "chromium",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + pdf_file.name,
        html_file_path,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file.name

# Define function to unzip and pdf
def unzip_and_pdf(zip_obj, comp_name):

    st.write(f"Processing {comp_name}...")

    file_name = zip_obj.name
    # folder_name = "/tmp/" + file_name + "_" + session_uuid
    
    zip_data = zip_obj.read()
    # Create a temp folder
    with tempfile.TemporaryDirectory() as folder_name:
        # Unzip the file
        with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
            zip_ref.extractall(folder_name) # Note that zip file needs to be extracted to local disk so that the css/images can work.
            
        # Get list of files in the directory (this only looks at the parent directory, not the subdirectories.)
        files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]

        for file in files:
            if file.endswith(".html"):  # Check if filename ends with ".html"
                st.write(f"...... processing {file}")
                pdf_path = html_to_pdf(folder_name + "/" + file)
                st.write(f"...... pdf path is {pdf_path}")
                pdf_files[comp_name + "_" + file.replace(".html",".pdf")] = pdf_path


pdf_files = OrderedDict() # To maintain insertion order, use this rather than a normal dictionary
if zip_1:
    unzip_and_pdf(zip_1, "covernote")
if zip_2:
    unzip_and_pdf(zip_2, "body")
if zip_3:
    unzip_and_pdf(zip_3, "annex")
if zip_4:
    unzip_and_pdf(zip_4, "distlist")


# For debugging
st.write(f"Individual pdf files...")
st.json(pdf_files)
for pdf_name, pdf_path in pdf_files.items():
    st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)


# Filter based on key presence and absence of "SMC" 
list_A4 = []
list_SMC = []
for key, value in pdf_files.items():
    if "index.pdf" in key and "SMC_index.pdf" not in key:
        list_A4.append(value)
    elif "SMC_index.pdf" in key:
        list_SMC.append(value)


# For debugging
st.write("Sorted into A4 and SMC pdfs...")
st.write(f"...A4 pdfs is {list_A4}")
st.write (f"...SMC pdfs is {list_SMC}")


# Combine the PDFs
def combine_pdfs(pdf_files):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    merger = PdfWriter()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(temp_file)
    merger.close()
    return temp_file.name

combined_A4 = combine_pdfs(list_A4)
combined_SMC = combine_pdfs(list_SMC)


# For debugging
st.write("Combined PDFs...")
st.download_button(label="combined_A4.pdf", data=open(combined_A4, 'rb').read(), file_name="combined_A4.pdf")
st.download_button(label="combined_SMC.pdf", data=open(combined_SMC, 'rb').read(), file_name="combined_SMC.pdf")






import os

def get_folder_size(path):
  """
  Calculates the total size of a directory and its subdirectories.

  Args:
      path: The path to the directory.

  Returns:
      The total size of the directory in bytes.
  """
  total_size = 0
  for root, _, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        total_size += os.path.getsize(file_path)
      except OSError:
        # Handle potential permission errors or other issues
        pass
  return total_size

# Example usage
folder_path = "/tmp"
folder_size = get_folder_size(folder_path)

# Convert to human-readable format (optional)
if folder_size > 1024**3:
  folder_size = folder_size / (1024**3)
  unit = "GB"
elif folder_size > 1024**2:
  folder_size = folder_size / (1024**2)
  unit = "MB"
elif folder_size > 1024:
  folder_size = folder_size / 1024
  unit = "KB"
else:
  unit = "bytes"

st.write(f"Total size of folder '{folder_path}': {folder_size:.2f} {unit}")



st.write("check tmp contents")
st.write(os.listdir("/tmp"))
