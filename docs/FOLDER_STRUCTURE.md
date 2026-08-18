# Mapeamento de Diretórios do Repositório

Abaixo está a disposição completa dos arquivos do Monolito Modular e pastas de suporte, detalhando a arquitetura interna de domínios isolados do Frontend (`modules`), infraestrutura compartilhada (`shared`) e o isolamento de rotas do Backend:

```text
.
├── app
│   ├── backend
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   └── src
│   │       ├── config.py
│   │       ├── __init__.py
│   │       ├── main.py
│   │       └── modules
│   │           ├── chat
│   │           │   ├── __init__.py
│   │           │   ├── router.py
│   │           │   └── service.py
│   │           ├── document
│   │           │   ├── __init__.py
│   │           │   ├── router.py
│   │           │   └── service.py
│   │           └── __init__.py
│   └── frontend
│       ├── index.html
│       ├── package.json
│       ├── README.md
│       ├── src
│       │   ├── App.vue
│       │   ├── main.ts
│       │   ├── modules
│       │   │   ├── chat
│       │   │   │   ├── components
│       │   │   │   │   └── ChatWindow.vue
│       │   │   │   └── views
│       │   │   │       └── ChatModule.vue
│       │   │   └── document
│       │   │       ├── components
│       │   │       │   └── FileUploader.vue
│       │   │       └── views
│       │   │           └── DocumentModule.vue
│       │   ├── shared
│       │   │   ├── api
│       │   │   │   └── client.ts
│       │   │   └── components
│       │   │       └── BaseLayout.vue
│       │   └── style.css
│       ├── tsconfig.json
│       └── vite.config.ts
├── docs
│   ├── ARCHITECTURE.md
│   ├── FOLDER_STRUCTURE.md
│   └── SYSTEM_TESTS.md
├── README.md
└── samples
    ├── dados_empresa.csv
    └── diretrizes_suporte.pdf
```
