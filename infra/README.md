# Alura Agente - Infrastructure & Configuration Management

> Camada central de infraestrutura, contendo as configurações de proxy reverso local, arquivos de variáveis e gerenciamento do provisionamento automatizado em nuvem.

Este diretório centraliza toda a inteligência de DevOps e engenharia de sistemas do **Alura Agente**. A estrutura está dividida em duas realidades complementares: o isolamento do ambiente de desenvolvimento local via containers e a orquestração automatizada da topologia de produção em nuvem.

---

## Estrutura do Diretório

A árvore de arquivos abaixo detalha a organização dos componentes de configuração de rede e arquivos de automação:

```text
infra/
├── README.md               # Este guia operacional da camada de infraestrutura
└── nginx/                  # Diretório de configuração do Proxy Reverso local
    └── default.conf        # Arquivo de regras de roteamento HTTP do Nginx local
```

*(Nota: Na raiz do seu repositório, encontram-se os arquivos globais de automação da infraestrutura como código (IaC) e scripts Shell que disparam os módulos adicionais):*

```text
.
├── main.tf                 # Orquestrador global e chamada dos módulos técnicos do Terraform
├── variables.tf            # Declaração de tipos de dados das variáveis globais da raiz
├── terraform.tfvars        # Arquivo privado contendo os tokens reais de acesso à nuvem
├── deploy.sh               # Shell script para automação da inicialização do ambiente
├── destroy.sh              # Shell script para automação da destruição total dos recursos
└── modules/                # Subpastas de encapsulamento de recursos por plataforma
    ├── render/             # Módulo de deploy do container Docker da API Python no Render
    └── vercel/             # Módulo de hospedagem edge do cliente web em Vue 3 na Vercel
```

---

## Descrição Detalhada dos Componentes

### 1. Servidor de Proxy Reverso (`infra/nginx/default.conf`)
O arquivo `default.conf` é o cérebro do roteamento de tráfego no ambiente de desenvolvimento local controlado pelo arquivo `docker-compose.yml`.
* **Objetivo:** Atuar como ponto único de entrada na porta padrão HTTP (80).
* **Comportamento:** Intercepta as requisições do usuário no navegador e faz o redirecionamento interno. Chamadas direcionadas para a raiz `/` carregam os arquivos estáticos do contêiner do Frontend, enquanto as requisições para os caminhos de API `/chat/`, `/document/` e `/api/health` sofrem um *proxy pass* transparente para o contêiner do Backend (FastAPI), mitigando qualquer barreira de CORS local.

### 2. Orquestração em Nuvem (`Terraform`)
Os arquivos do Terraform na raiz gerenciam o ciclo de vida dos recursos de produção na internet de forma declarativa e modular:

* **`main.tf` (Orquestrador Raiz):** Liga os módulos entre si. Ele lê o token do Hugging Face e repassa o dado de forma segura para dentro do módulo do Render, além de capturar o endpoint público gerado pela API e injetá-lo dinamicamente no frontend da Vercel.
* **`modules/render/`:** Configura o serviço de aplicação web no Render no formato `docker`, lendo o arquivo `Dockerfile` na pasta do backend e gerando o build automático do contêiner Python com injeção de ambiente para as credenciais do Hugging Face.
* **`modules/vercel/`:** Provisiona o cliente estático na Vercel, embutindo a variável `VITE_API_BASE_URL` apontando para o Render e associando o repositório GitHub para gerar automação a cada atualização na branch principal.

---

## Fluxo Operacional de Execução

O ciclo completo de operação desta camada está segmentado em dois escopos distintos:

### Execução em Desenvolvimento (Local)
O arquivo de proxy do Nginx é montado como um volume de leitura dentro da malha do Docker Compose. Nenhuma ação direta é necessária neste diretório para rodar localmente, bastando acionar o comando na raiz do projeto:
```bash
docker compose up --build -d
```

### Execução em Produção (Nuvem)
Para disparar, modificar ou destruir o ambiente estável nas nuvens de forma ágil através dos scripts automatizados criados na raiz, utilize os comandos correspondentes no terminal:
```bash
# Para subir toda a infraestrutura e realizar o deploy do RAG na nuvem
./deploy.sh

# Para remover e limpar todos os serviços ativos no Render e na Vercel
./destroy.sh
```
