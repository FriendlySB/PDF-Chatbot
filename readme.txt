Cara menggunakan Chatbot

Chatbot kami memerlukan library sebagai berikut:
langchain==0.1.11
numpy==1.25.2
Pillow==10.2.0
protobuf==4.25.3
streamlit==1.31.1
streamlit_chat==0.1.1
tornado==6.1
transformers==4.26.1
pymupdf
sentence-transformers
faiss-cpu
llama-cpp-python

Library tersebut perlu diinstall terlebih dahulu pada environment python yang akan menjalakan program kami.

Struktur Folder

.streamlit
    config.toml
model
    llama-2-7b-chat.Q4_K_M.gguf
vectorstore
    db_faiss
        index.faiss
        index.pkl
app.py
fileingestor.py
loadllm.py
readme.txt
requirements.txt

Tahap penggunaan
1. Download model kami pada link Google Drive berikut :
2. Clone atau download source code kami dari github pada link github berikut :
3. Di dalam folder PDF-Chatbot, buat sebuah folder bernama model
4. Pindahkan model yang telah didownload ke dalam folder tersebut
5. Untuk menjalankan aplikasi, buka command prompt
6. Lakukan perintah cd atau change directory ke path dimana folder PDF-Chatbot disimpan
7. Jalankan perintah streamlit run app.py
8. Program akan membuka sebuah tab browser baru dimana aplikasi chatbot akan dijalankan
9. Chatbot siap digunakan
