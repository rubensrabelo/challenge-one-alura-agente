# Mapeamento de Diretórios do Repositório

Abaixo está a disposição completa dos arquivos do Monolito Modular e pastas de suporte, detalhando a arquitetura interna de domínios isolados do Frontend (`modules`), infraestrutura compartilhada (`shared`), o isolamento de rotas do Backend e a malha de arquivos de configuração de infraestrutura contêinerizada e arquivos IaC do Terraform:

```text
.
├── app
│   ├── backend
│   │   ├── Dockerfile
│   │   ├── faiss_index
│   │   │   ├── index.faiss
│   │   │   └── index.pkl
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
│   │           └── document
│   │               ├── __init__.py
│   │               ├── router.py
│   │               └── service.py
│   └── frontend
│       ├── Dockerfile
│       ├── index.html
│       ├── package.json
│       ├── package-lock.json
│       ├── public
│       │   └── assistente-de-robo.png
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
│       ├── tsconfig.app.json
│       ├── tsconfig.json
│       ├── tsconfig.node.json
│       └── vite.config.ts
├── docker-compose.yml
├── .env.example
├── docs
│   ├── ARCHITECTURE.md
│   ├── FOLDER_STRUCTURE.md
│   └── SYSTEM_TESTS.md
├── infra
│   ├── nginx
│   │   └── default.conf
│   ├── README.md
│   └── terraform
│       ├── main.tf
│       ├── modules
│       │   ├── render
│       │   │   ├── main.tf
│       │   │   ├── outputs.tf
│       │   │   └── variables.tf
│       │   └── vercel
│       │       ├── main.tf
│       │       ├── outputs.tf
│       │       └── variables.tf
│       ├── outputs.tf
│       ├── providers.tf
│       ├── terraform.tfvars
│       ├── terraform.tfvars.example
│       └── variables.tf
├── README.md
├── samples
│   ├── dados_empresa.csv
│   └── diretrizes_suporte.pdf
└── scripts
    ├── deploy.sh
    └── destroy.sh
```
