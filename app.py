# Import streamlit sebagai framework untuk aplikasi ini
import streamlit as st

from fileingestor import FileIngestor

# Set the title for the Streamlit app
# Mengatur judul dan subjudul untuk tampilan aplikasi nantinya

st.title("Chat with PDF")
st.write("Powered by Llama2")

# Create a file uploader in the sidebar
# Membuat sidebar dimana file pdf yang akan digunakan oleh chatbot bisa diupload
uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")

# Jika file telah diupload, maka panggil class FileIngestor yang akan mengolah file PDF yang telah disubmit
if uploaded_file:
    file_ingestor = FileIngestor(uploaded_file)
    file_ingestor.handlefileandingest()