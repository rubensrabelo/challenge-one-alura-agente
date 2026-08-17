import os
import shutil
import logging
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from src.config import UPLOAD_DIR, VECTOR_DB_DIR, embeddings_model

logger = logging.getLogger(__name__)

class DocumentService:
    @staticmethod
    async def process_and_index(file: UploadFile) -> str:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        loader = PyPDFLoader(file_path) if file.filename.endswith('.pdf') else CSVLoader(file_path)
        raw_documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
        split_docs = text_splitter.split_documents(raw_documents)
        
        logger.info(f"Salvando índice FAISS no caminho: {VECTOR_DB_DIR}")
        
        if os.path.exists(VECTOR_DB_DIR) and os.path.exists(os.path.join(VECTOR_DB_DIR, "index.faiss")):
            vector_store = FAISS.load_local(VECTOR_DB_DIR, embeddings_model, allow_dangerous_deserialization=True)
            vector_store.add_documents(split_docs)
        else:
            vector_store = FAISS.from_documents(split_docs, embeddings_model)
            
        vector_store.save_local(VECTOR_DB_DIR)
        return f"O documento '{file.filename}' foi processado e indexado com sucesso."
