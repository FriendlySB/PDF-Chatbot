# Import streamlit, langchanin, PyMuPDFLoader, dan file loadllm
# PyMuPDFLoader adalah library untuk mengekstraksi, menganalisa, dan mengkonversi data dari dokumen PDF
import streamlit as st
from langchain.document_loaders import PyMuPDFLoader
from loadllm import Loadllm
from streamlit_chat import message
import tempfile
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

# Load model directly
#from transformers import AutoModel

# Path dimana hasil vectore score dari FAISS akan disimpan
# FAISS (Facebook AI Similarity Search) adalah sebuah library untuk mencari embedding dalam dokumen yang serupa satu dengan yang lainnya
# FAISS mempunyai algoritma yang mencari kesamaan di set vector dengan ukuran apapun
DB_FAISS_PATH = 'vectorstore/db_faiss'

class FileIngestor:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file

    def handlefileandingest(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(self.uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyMuPDFLoader(file_path=tmp_file_path)
        data = loader.load()

        # Create embeddings using Sentence Transformers
        # Word embedding dari dokumen akan dibuat menggunakan sentence-transformers yang disediakan HuggingFace
        # Transformer ini berbasis BERT dan bisa memetakan kalimat dan paragraf menjadi vector space dengan 
        # densitas 384 dimensi
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

        # Create a FAISS vector store and save embeddings
        db = FAISS.from_documents(data, embeddings)
        db.save_local(DB_FAISS_PATH)

        # Load the language model
        # Load model Llama 2 yang telah disiapkan di file loadllm.py
        llm = Loadllm.load_llm()
        #llm = AutoModel.from_pretrained("TheBloke/Llama-2-7B-Chat-GGUF")

        # Create a conversational chain
        # Membuat chain conversation dari Llama 2
        chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

        # Function for conversational chat
        # Memasukkan chat baru bagi Streamlit
        # Query adalah pertanyaan yang kita berikan, answer jawaban, dan history agar Llama mengetahui
        # konteks untuk percakapan kita dengan dia
        def conversational_chat(query):
            result = chain({"question": query, "chat_history": st.session_state['history']})
            st.session_state['history'].append((query, result["answer"]))
            return result["answer"]

        # Initialize chat history
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        # Initialize messages
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello ! Ask me(LLAMA2) about " + self.uploaded_file.name + " 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! 👋"]

        # Create containers for chat history and user input
        # Buat container untuk display UI
        response_container = st.container()
        container = st.container()

        # User input form
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Query:", placeholder="Talk to PDF data 🧮", key='input')
                submit_button = st.form_submit_button(label='Send')

            # Jika kita mengklik tombol submit/enter dan user input telah diisi, maka conversation akan kita mulai
            if submit_button and user_input:
                output = conversational_chat(user_input)
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        # Display chat history
        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")