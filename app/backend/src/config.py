import os
import logging
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEndpointEmbeddings, ChatHuggingFace

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BACKEND_ROOT, "stored_docs")
VECTOR_DB_DIR = os.path.join(BACKEND_ROOT, "faiss_index")

os.makedirs(UPLOAD_DIR, exist_ok=True)

logger.info(f"Diretório de Vetores configurado em: {VECTOR_DB_DIR}")

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

embeddings_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)

llm_base = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-1.5B-Instruct:featherless-ai",
    huggingfacehub_api_token=hf_token,
    task="text-generation",  
    max_new_tokens=512,
    temperature=0.1
)

llm_model = ChatHuggingFace(llm=llm_base)
