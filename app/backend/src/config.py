import os
import logging
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEndpointEmbeddings

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "stored_docs")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "faiss_index")

os.makedirs(UPLOAD_DIR, exist_ok=True)

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    logger.error("HUGGINGFACEHUB_API_TOKEN não foi encontrado no arquivo .env!")

# 1. Embeddings via API (Serverless)
logger.info("Configurando Hugging Face Inference API para Embeddings...")
embeddings_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)

# 2. LLM via API (Serverless - Usando um modelo rápido e excelente para chat/RAG)
logger.info("Configurando Hugging Face Inference API para LLM (Mistral-7B-Instruct)...")
llm_model = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=hf_token,
    task="text-generation",
    max_new_tokens=512,
    temperature=0.1,
    do_sample=False
)
