# Challenge Alura Agente - Sistema RAG Open-Source (Hugging Face & OCI)

Este projeto consiste em um Agente Inteligente baseado na arquitetura RAG (Retrieval-Augmented Generation) utilizando tecnologia open-source do ecossistema Hugging Face consumida via API Serverless. O sistema processa documentos nos formatos PDF e CSV, indexa-os localmente em um banco de vetores e responde a perguntas em linguagem natural por meio de uma interface de chat moderna.

## Documentação do Projeto

Para facilitar a manutenção e o entendimento do Monolito Modular, a documentação foi dividida em seções especializadas:

*   **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Detalhamento do fluxo de dados unificado entre Frontend e Backend por meio de diagramas Mermaid estruturados.
*   **[FOLDER_STRUCTURE.md](docs/FOLDER_STRUCTURE.md)**: Visualização completa da árvore de arquivos do Monolito Modular seguindo a divisão de domínios isolados e camadas compartilhadas.
*   **[SYSTEM_TESTS.md](docs/SYSTEM_TESTS.md)**: Passo a passo para iniciar o Frontend (Vue 3) e o Backend (FastAPI) localmente, acompanhado de roteiros práticos de testes utilizando os arquivos de amostra (PDF/CSV).

---

## Subprojetos

Acesse também os guias específicos de configuração de cada camada do desenvolvimento:
*   **[Documentação Técnica do Backend (FastAPI)](app/backend/README.md)**
*   **[Documentação Técnica do Frontend (Vue 3)](app/frontend/README.md)**
