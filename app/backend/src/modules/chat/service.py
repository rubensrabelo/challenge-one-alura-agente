import os
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.config import VECTOR_DB_DIR, embeddings_model, llm_model

class ChatService:
    @staticmethod
    def answer_question(question: str) -> str:
        if not os.path.exists(VECTOR_DB_DIR):
            raise ValueError("A base de conhecimento está vazia. Faça upload de arquivos primeiro.")
            
        vector_store = FAISS.load_local(VECTOR_DB_DIR, embeddings_model, allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        system_prompt = (
            "Você é o Agente Virtual do Challenge Alura. Responda à pergunta usando apenas o contexto fornecido.\n"
            "Se não souber, diga: 'Desculpe, não encontrei essa informação nos documentos carregados.'\n\n"
            "Contexto:\n{context}"
        )
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        combine_docs_chain = create_stuff_documents_chain(llm_model, prompt_template)
        rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
        
        result = rag_chain.invoke({"input": question})
        return result["answer"]
