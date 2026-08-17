# Challenge Alura Agente - Sistema RAG Open-Source (Hugging Face & OCI)

Este projeto consiste em um Agente Inteligente baseado na arquitetura RAG (*Retrieval-Augmented Generation*) utilizando tecnologia 100% open-source do ecossistema **Hugging Face**. O sistema processa documentos nos formatos PDF e CSV, indexa-os localmente em um banco de vetores e responde a perguntas em linguagem natural por meio de uma interface de chat moderna.

## Arquitetura do Sistema: Monolito Modular
A solução adota o padrão de **Monolito Modular** centralizado dentro do diretório `app/`, garantindo portabilidade para nuvem e desacoplamento de domínios:

*   **`app/backend/`**: API REST construída com **FastAPI**. Gerencia o upload de arquivos, orquestração de prompts via **LangChain**, geração de embeddings locais com `sentence-transformers` e indexação semântica via **FAISS**.
*   **`app/frontend/`**: Interface de página única (SPA) rica e reativa em **Vue 3 (Composition API)**.

---

## Stack Tecnológica (Open-Source)

*   **Framework API**: FastAPI (Assíncrono, Type Hints)
*   **Interface**: Vue 3 (Script Setup)
*   **Orquestração de IA**: LangChain & Hugging Face Pipeline
*   **Modelo de Embedding**: `sentence-transformers/all-MiniLM-L6-v2` (Local, leve e veloz)
*   **Modelo de Inferência (LLM)**: Modelos open-source via Hugging Face Inference API ou Local Pipeline (ex: Llama-3, Mistral ou Qwen)
*   **Banco de Vetores**: FAISS (Facebook AI Similarity Search)
*   **Infraestrutura Cloud**: Oracle Cloud Infrastructure (OCI) Compute Instance

---

## Como Executar o Backend Localmente

### Pré-requisitos
* Python 3.10 ou superior instalado.
* Compilador C++ (necessário para compilação local do FAISS em alguns sistemas).

### Passo a Passo
1. Navegue até o diretório do backend:
   ```bash
   cd app/backend
   ```

2. Crie e ative o seu ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo de variáveis de ambiente:
   * Crie o arquivo `.env` com base no modelo do repositório.

5. Inicialização:
   *(O comando exato de inicialização será adicionado assim que criarmos o arquivo main.py)*
