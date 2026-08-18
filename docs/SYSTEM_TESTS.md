# Guia de Execução e Homologação de Testes (Local e Nuvem)

Siga as instruções abaixo para gerenciar e validar o ciclo de vida completo do ecossistema, utilizando o Docker Compose para o ambiente local controlado ou os scripts de automação IaC para o provisionamento em nuvem na Vercel e no Render.

---

## 1. Execução no Ambiente Local (Docker)

### Pré-requisitos
* Docker e Docker Compose instalados na máquina.
* Token de Acesso de leitura válido da Hugging Face.

### Inicialização do Ambiente
1. Certifique-se de que o arquivo `.env` está criado na raiz do repositório (ao lado do `docker-compose.yml`) contendo a sua chave de acesso:
   ```env
   HUGGINGFACEHUB_API_TOKEN=hf_seu_token_real_aqui
   VITE_API_BASE_URL=http://localhost
   PORT=8000
   HOST=0.0.0.0
   ```
2. Execute o comando abaixo no terminal na raiz do projeto para construir as imagens locais e inicializar os serviços em segundo plano:
   ```bash
   docker compose up --build -d
   ```
3. Valide se todos os contêineres (`alura_agente_backend`, `alura_agente_frontend` e `alura_agente_proxy`) inicializaram com sucesso rodando:
   ```bash
   docker compose ps
   ```
4. Abra o seu navegador e acesse a aplicação unificada diretamente no endereço padrão HTTP: `http://localhost`

---

## 2. Execução no Ambiente Nuvem (Scripts Automáticos)

### Pré-requisitos
* Terraform instalado na máquina de desenvolvimento.
* Arquivo `terraform.tfvars` configurado na raiz contendo os tokens e credenciais reais do Render, Vercel e Hugging Face.

### Deploy Automatizado
1. Garanta a permissão de execução nos scripts utilitários localizados na raiz do projeto:
   ```bash
   chmod +x deploy.sh destroy.sh
   ```
2. Dispare o script de inicialização para planejar e aplicar automaticamente toda a infraestrutura multicloud:
   ```bash
   ./deploy.sh
   ```
3. O Terraform provisionará a API do Python no Render injetando o token de inferência de IA e hospedará o frontend estático Vue 3 na infraestrutura da Vercel. Ao término da execução, as URLs públicas geradas serão exibidas no terminal.
4. Acesse o link público fornecido pela Vercel em seu navegador.

### Destruição do Ambiente
Para remover completamente todos os recursos alocados na nuvem e evitar cobranças indesejadas, execute o script de encerramento automático:
```bash
./destroy.sh
```

---

## 3. Roteiro Prático de Testes Baseado na Pasta Samples

Seja no ambiente local (`http://localhost`) ou na nuvem (`https://vercel.app`), certifique-se de que o indicador visual no cabeçalho exiba a mensagem verde **"Backend Conectado"** antes de iniciar as validações abaixo.

### Cenário A: Homologação do Arquivo PDF (`samples/diretrizes_suporte.pdf`)
1. Arraste o arquivo `diretrizes_suporte.pdf` para a área de upload à esquerda.
2. Aguarde a mensagem de confirmação de indexação bem-sucedida do banco vetorial FAISS.
3. Insira as seguintes perguntas no chat para validar as respostas com base no documento:

*   **Pergunta 1:** `Como funciona o horário de atendimento do suporte técnico para o plano Individual?`
    *   **Resposta Esperada:** Deve indicar que o atendimento ocorre de segunda a sexta-feira, das 08:00 às 18:00, via o e-mail suporte@aluraagente.com.br.
*   **Pergunta 2:** `Qual é o prazo para solicitar o reembolso total e quanto tempo demora o estorno no Pix?`
    *   **Resposta Esperada:** Deve citar o prazo estrito de até 7 dias corridos e o tempo de processamento de até 2 dias úteis para Pix.
*   **Pergunta 3:** `O suporte pode me pedir a senha ou token pelo WhatsApp em alguma situação?`
    *   **Resposta Esperada:** Deve declarar explicitamente que nenhum funcionário solicitará senhas ou tokens por aplicativos de mensagem.

### Cenário B: Homologação do Arquivo CSV (`samples/dados_empresa.csv`)
1. Realize o upload do arquivo `dados_empresa.csv` na mesma área de arraste para mesclar os dados tabulares ao banco de vetores ativo.
2. Envie as perguntas estruturadas na caixa de chat:

*   **Pergunta 1:** `Qual é o preço do Notebook Pro 15 e quantas unidades temos em estoque?`
    *   **Resposta Esperada:** O preço é 4500.00 e o estoque possui 12 unidades.
*   **Pergunta 2:** `Onde fica a Cadeira Ergonômica e qual o valor dela?`
    *   **Resposta Esperada:** Fica localizada no Corredor B e custa 1200.00.
*   **Pergunta 3:** `Qual produto está localizado no Depósito Central e qual a quantidade dele em estoque?`
    *   **Resposta Esperada:** É a Mesa Digitalizadora, com 0 unidades em estoque.

### Cenário C: Teste de Blindagem Semântica contra Alucinações
Envie uma pergunta de escopo totalmente alheio aos documentos carregados para validar as diretivas de restrição e segurança do sistema RAG:

*   **Pergunta:** `Como faço para assar um bolo de chocolate tradicional?`
    *   **Resposta Esperada:** O sistema deve recusar a geração de conteúdo fora de contexto e retornar estritamente o texto padrão configurado: `Desculpe, não encontrei essa informação nos documentos carregados.`
