# Arquitetura do Sistema e Stack Tecnológica

O sistema adota o padrão de **Monolito Modular**, centralizado dentro do diretório `app/`, buscando manter os domínios desacoplados e facilitar a evolução e implantação em ambiente cloud. A comunicação entre o cliente e o servidor é realizada por meio de requisições assíncronas HTTP/JSON.

## Fluxo de Dados Unificado

O diagrama abaixo apresenta o fluxo principal do sistema, desde a interação do usuário com a interface até o processamento dos documentos e das consultas utilizando RAG.

```mermaid
flowchart TB
    U([Usuário])

    subgraph FRONT["Frontend · Vue 3"]
        UI["Interface"]
        DOC["Document Module"]
        CHAT["Chat Module"]
        API["API Client · Axios"]

        UI --> DOC
        UI --> CHAT
        DOC --> API
        CHAT --> API
    end

    subgraph BACK["Backend · FastAPI"]
        MAIN["API"]
        UPLOAD["POST /document/upload"]
        ASK["POST /chat/ask"]
        SPLIT["Text Splitter"]
        RAG["RAG Pipeline · LCEL"]

        MAIN --> UPLOAD
        MAIN --> ASK
        UPLOAD --> SPLIT
        ASK --> RAG
    end

    subgraph AI["IA & Dados"]
        EMB["Hugging Face<br/>Embeddings"]
        FAISS[("FAISS<br/>Vector Store")]
        LLM["Hugging Face<br/>Qwen2.5 LLM"]
        DOCS[("Stored Documents")]
    end

    U --> UI
    API --> MAIN

    UPLOAD --> DOCS
    SPLIT --> EMB
    EMB --> FAISS

    RAG --> FAISS
    FAISS --> RAG
    RAG --> LLM
    LLM --> RAG

    ASK --> RAG
    RAG --> ASK
    ASK --> API
    API --> CHAT

    classDef frontend fill:#e8f4fd,stroke:#2196f3,stroke-width:2px,color:#111
    classDef backend fill:#eaf7ea,stroke:#43a047,stroke-width:2px,color:#111
    classDef ai fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#111
    classDef data fill:#f3e8ff,stroke:#8e44ad,stroke-width:2px,color:#111
    classDef user fill:#f5f5f5,stroke:#555,stroke-width:2px,color:#111

    class U user
    class UI,DOC,CHAT,API frontend
    class MAIN,UPLOAD,ASK,SPLIT,RAG backend
    class EMB,LLM ai
    class FAISS,DOCS data
```

### Fluxo principal

**Upload de documentos**

`Usuário → Vue → FastAPI → Text Splitter → Embeddings → FAISS`

**Pergunta ao sistema**

`Usuário → Vue → FastAPI → RAG → FAISS → Qwen2.5 → Resposta`

## Stack Tecnológica

* **Framework API**: FastAPI (Assíncrono, Type Hints, Pydantic v2)
* **Interface**: Vue 3 (Script Setup) + Vite
* **Linguagem & Estilização**: TypeScript + Tailwind CSS v4 (Oxide Engine)
* **Biblioteca de Ícones**: Lucide Vue Next
* **Orquestração de IA**: LangChain via LCEL (Runnables & Pipes)
* **Motor de IA**: Hugging Face Inference API

  * **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
  * **LLM (Inferência RAG)**: `Qwen/Qwen2.5-1.5B-Instruct:featherless-ai`
* **Banco de Vetores**: FAISS (Facebook AI Similarity Search)
* **Infraestrutura Cloud**: Oracle Cloud Infrastructure (OCI) Compute Instance
