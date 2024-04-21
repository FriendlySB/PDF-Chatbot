# Import library langchain
# Langchain adalah framework untuk mempermudah pembuatan aplikasi dengan menggunakan Large Language Models (LLM) seperti
# GPT, Claude, Llama, dan banyak LLM lainnya
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Path dimana file model Llama yang digunakan sebagai chatbot disimpan
# Model yang kami gunakan adalah Llama 2 7B Chat GGUF yang merupakan modifikasi dari Llama 2 7B Chat yang dibuat oleh Meta
# Model ini dimodifikasi untuk menggunakan format GGUF yang menawarkan beberapa keuntungan dari tipe lama GGML seperti
# tokenization yang lebih baik, support untuk token special, support untuk metadata, dan didesain extensible
model_path = 'model/llama-2-7b-chat.Q4_K_M.gguf'

class Loadllm:
    @staticmethod
    # Function untuk meload model Llama 2 dan menyiapkannya untuk digunakan
    def load_llm():
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        # Prepare the LLM

        # LlamaCpp adalah sebuah library yang bertujuan unutk memberikan LLM inference dengan setup minimal dan performa
        # state of the art pada berbagai macam hardware, baik local, maupun di cloud
        # model_path = Tempat dimana model Llama disimpan di komputer
        # n_gpu_layers = Jumlah layer yang akan dioffload ke GPU
        # n_batch = Ukuran batch maximum untuk pemrosesan prompt
        # n_ctx = Text context
        # max_tokens = Jumlah maximum token yang akan digenerate sebagai respons oleh model
        # local_files_only = Apakah hanya menggunakan file model yang ada secara lokal saja atau akan mendownload dari luar
        # f16_kv
        # callback_manager
        # verbose = Print output verbose
        llm = LlamaCpp(
            model_path=model_path,
            n_gpu_layers=-1,
            n_batch=512,
            n_ctx=4096,
            max_tokens=256,
            local_files_only = True,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            callback_manager=callback_manager,
            verbose=True,
        )
        # Return model Llama yang telah siap
        print("Done Loading Model")
        return llm