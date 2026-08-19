# Arquitetura do Sistema e Stack Tecnológica

O sistema adota o padrão de **Monolito Modular**, centralizado dentro do diretório `app/`, buscando manter os domínios desacoplados e facilitar a evolução e implantação em ambiente cloud. A comunicação entre o cliente e o servidor é realizada por meio de requisições assíncronas HTTP/JSON.

## Fluxo de Dados Unificado

O fluxo principal do sistema mapeia a jornada dos dados desde a interação do usuário com a interface até o processamento dos documentos e das consultas utilizando RAG.

### Ambiente Local (Docker Compose & Nginx Proxy)

O diagrama abaixo apresenta a topologia contêinerizada local, destacando o papel do `nginx_proxy` no roteamento de chamadas e no consumo do volume compartilhado de assets estáticos:

```mermaid
flowchart TB
    U([Usuário])

    subgraph PROXY["Gateway · Nginx Proxy Container"]
        NGX["Nginx Server"]
        CONF["default.conf"]
        NGX --- CONF
    end

    subgraph FRONT["Frontend · Vue 3 Container"]
        UI["Interface"]
        DOC["Document Module"]
        CHAT["Chat Module"]
        API["API Client · Axios"]

        UI --> DOC
        UI --> CHAT
        DOC --> API
        CHAT --> API
    end

    subgraph VOL["Volumes Compartilhados"]
        V_DIST[("frontend_dist<br/>Static Assets")]
    end

    subgraph BACK["Backend · FastAPI Container"]
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

    subgraph AI["IA & Dados Externos"]
        EMB["Hugging Face<br/>Embeddings"]
        FAISS[("FAISS<br/>Vector Store")]
        LLM["Hugging Face<br/>Qwen2.5 LLM"]
        DOCS[("Stored Documents")]
    end

    %% Fluxo de Inicialização e Assets
    API -.->|Build/Dist| V_DIST
    V_DIST -.->|Read Static| NGX

    %% Fluxo de Tráfego do Usuário
    U -->|Acessa Porta 80| NGX
    NGX -->|Entrega HTML/SPA| U
    NGX -->|Proxy /chat/ e /document/| MAIN

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

    classDef frontend fill:#e8f4fd,stroke:#2196f3,stroke-width:2px,color:#111
    classDef backend fill:#eaf7ea,stroke:#43a047,stroke-width:2px,color:#111
    classDef ai fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#111
    classDef data fill:#f3e8ff,stroke:#8e44ad,stroke-width:2px,color:#111
    classDef user fill:#f5f5f5,stroke:#555,stroke-width:2px,color:#111
    classDef proxy fill:#eceff1,stroke:#607d8b,stroke-width:2px,color:#111

    class U user
    class UI,DOC,CHAT,API frontend
    class MAIN,UPLOAD,ASK,SPLIT,RAG backend
    class EMB,LLM ai
    class FAISS,DOCS,V_DIST data
    class NGX,CONF proxy
```

### Ambiente Nuvem (Vercel & Render via Terraform)

A topologia em nuvem representa o ecossistema gerenciado de produção atual. Os recursos são instanciados via Terraform e integrados de forma totalmente serverless:

```mermaid
flowchart TD
    U([Usuário])
    
    subgraph VC["Infraestrutura Edge · Vercel"]
        VF["Frontend Web App"]
        V_ENV["VITE_API_BASE_URL"]
        VF --- V_ENV
    end

    subgraph RD["Infraestrutura Gerenciada · Render"]
        RB["Backend API (FastAPI)"]
        R_ENV["HUGGINGFACEHUB_API_TOKEN"]
        R_VOL[("Efêmero<br/>FAISS Indexes")]
        
        RB --- R_ENV
        RB --- R_VOL
    end

    subgraph HF["Hugging Face Cloud Serverless"]
        API_E["Inference API: Embeddings"]
        API_L["Inference API: Qwen2.5 LLM"]
    end

    U -->|Acessa Interface HTTPS| VF
    VF -->|Requisições CORS Seguras| RB
    RB <-->|HTTPS Hub Tokens| HF

    classDef cloud_f fill:#e8f4fd,stroke:#2196f3,stroke-width:2px,color:#111
    classDef cloud_b fill:#eaf7ea,stroke:#43a047,stroke-width:2px,color:#111
    classDef cloud_ai fill:#fafafa,stroke:#9e9e9e,stroke-width:2px,color:#111
    classDef user fill:#f5f5f5,stroke:#555,stroke-width:2px,color:#111

    class U user
    class VF,V_ENV cloud_f
    class RB,R_ENV,R_VOL cloud_b
    class HF,API_E,API_L cloud_ai
```

---

## Fluxo Principal de Negócio

### Upload de documentos
* **Local:** `Usuário → Nginx Proxy → FastAPI → Text Splitter → Embeddings → FAISS`
* **Nuvem:** `Usuário → Vercel (Vue 3) → Render (FastAPI) → Text Splitter → Embeddings → FAISS (Memória/Disco Efêmero)`

### Pergunta ao sistema
* **Local:** `Usuário → Nginx Proxy → FastAPI → RAG → FAISS → Qwen2.5 → Resposta`
* **Nuvem:** `Usuário → Vercel (Vue 3) → Render (FastAPI) → RAG → FAISS → Qwen2.5 → Resposta`

---

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
* **Infraestrutura Cloud**: Servidores Serverless Dedicados (Vercel Edge Network + Render Web Services)
* **Ferramenta de Provisionamento (IaC)**: Terraform (Módulos `render` e `vercel`)
