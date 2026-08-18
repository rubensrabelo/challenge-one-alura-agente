# Alura Agente - Backend REST API (FastAPI & LangChain)

Este subprojeto engloba a camada de persistência, ingestão de dados e orquestração de Inteligência Artificial do sistema Alura Agente. A API foi desenhada seguindo os princípios de alta performance assíncrona, validação rigorosa de tipos e isolamento modular de regras de negócio.

## Tecnologias e Dependências Principais

*   **FastAPI & Uvicorn**: Framework web de alto desempenho baseado em Starlette e Pydantic v2 para tipagem de dados.
*   **LangChain & LCEL**: Biblioteca para encadeamento estruturado de componentes de IA através de pipes (|) utilizando sintaxe assíncrona declarativa.
*   **LangChain Hugging Face**: Conexão nativa serverless para geração de vetores e inferência textual.
*   **FAISS (CPU)**: Banco de dados vetorial de alta performance armazenado em disco de forma local na instância do servidor.
*   **PyPDF & Python-Multipart**: Extração de texto bruto de binários PDF e decodificação de fluxos de arquivos recebidos via requisições HTTP.

---

## Estrutura de Módulos (Domínios Isolados)

O backend divide-se em domínios de negócio autônomos dentro de `src/modules/`:

### Módulo Document (`src/modules/document/`)
*   `router.py`: Expõe o endpoint `POST /document/upload` recebendo o arquivo por streaming.
*   `service.py`: 
    1. Lê arquivos PDF (via `PyPDFLoader`) ou tabelas CSV (via `CSVLoader`).
    2. Aplica o `RecursiveCharacterTextSplitter` (tamanho de bloco de 1000 caracteres e sobreposição de 200).
    3. Gera os vetores utilizando o modelo `sentence-transformers/all-MiniLM-L6-v2`.
    4. Grava os índices em disco no diretório raiz `faiss_index/`.

### Módulo Chat (`src/modules/chat/`)
*   `router.py`: Expõe o endpoint `POST /chat/ask` aceitando um corpo JSON validado via Pydantic (`question`).
*   `service.py`: 
    1. Carrega o banco vetorial FAISS do disco.
    2. Executa a busca por similaridade de cosseno retornando os 3 blocos de texto mais relevantes.
    3. Injeta o contexto coletado em um prompt estruturado do sistema (System Prompt), bloqueando o LLM de inventar respostas falsas (alucinações).
    4. Dispara a requisição para o endpoint serverless do modelo `Qwen/Qwen2.5-1.5B-Instruct:featherless-ai`.

---

## Endpoints da API

A documentação interativa completa do Swagger fica disponível em `http://localhost:8000/docs`.

### 1. Ingestão de Documentos
*   **Rota**: `POST /document/upload`
*   **Payload**: `FormData` contendo a chave `file` (arquivo binário `.pdf` ou `.csv`).
*   **Resposta (201 Created)**:
    ```json
    {
      "message": "Documento indexado e mesclado ao banco vetorial FAISS com sucesso."
    }
    ```

### 2. Pipeline de Consulta RAG
*   **Rota**: `POST /chat/ask`
*   **Payload (JSON)**:
    ```json
    {
      "question": "Como funciona o horário de atendimento do suporte técnico?"
    }
    ```
*   **Resposta (200 OK)**:
    ```json
    {
      "answer": "Para clientes do plano Individual, o horário de atendimento é de segunda a sexta-feira, das 08:00 às 18:00..."
    }
    ```

### 3. Monitoramento de Saúde (Health Check)
*   **Rota**: `GET /`
*   **Resposta (200 OK)**:
    ```json
    {
      "status": "healthy"
    }
    ```
