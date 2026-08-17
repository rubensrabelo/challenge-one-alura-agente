import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
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
            "Se não souber a resposta com base no contexto, responda estritamente: 'Desculpe, não encontrei essa informação nos documentos carregados.'\n\n"
            "Contexto de Apoio:\n{context}\n\n"
            "Pergunta do Usuário: {question}"
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
