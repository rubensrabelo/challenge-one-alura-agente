import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import VECTOR_DB_DIR, embeddings_model, llm_model

logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    def answer_question(question: str) -> str:
        logger.info(f"Procurando índice FAISS no caminho: {VECTOR_DB_DIR}")
        
        if not os.path.exists(VECTOR_DB_DIR) or not os.path.exists(os.path.join(VECTOR_DB_DIR, "index.faiss")):
            logger.error(f"Índice FAISS não localizado em: {VECTOR_DB_DIR}")
            raise ValueError("A base de conhecimento está vazia ou corrompida. Faça upload de arquivos primeiro.")
            
        try:
            vector_store = FAISS.load_local(VECTOR_DB_DIR, embeddings_model, allow_dangerous_deserialization=True)
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            
            system_prompt = (
                "Você é o Agente Virtual do Challenge Alura. Responda à pergunta usando apenas o contexto fornecido.\n"
                "Se não souber a resposta com base no contexto, responda estritamente: 'Desculpe, não encontrei essa informação nos documentos carregados.'\n\n"
                "Contexto:\n{context}\n\n"
                "Pergunta: {question}"
            )
            
            prompt_template = ChatPromptTemplate.from_template(system_prompt)
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            rag_chain = (
                {
                    "context": retriever | format_docs, 
                    "question": RunnablePassthrough()
                }
                | prompt_template
                | llm_model
                | StrOutputParser()
            )
            
            answer = rag_chain.invoke(question)
            return answer
            
        except Exception as e:
            logger.error(f"Erro ao ler banco de vetores ou processar LLM: {str(e)}")
            raise e
