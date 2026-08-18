# Guia de Execução e Homologação de Testes (Ambiente Contêinerizado)

Siga as instruções abaixo para subir o ecossistema completo utilizando o Docker Compose e executar a homologação do pipeline RAG por meio dos arquivos de teste controlados.

## 1. Como Executar a Aplicação com Docker

### Pré-requisitos
* Docker e Docker Compose instalados na máquina.
* Token de Acesso de leitura válido da Hugging Face.

### Inicialização do Ambiente
1. Certifique-se de que o arquivo `.env` está criado na raiz do repositório (ao lado do `docker-compose.yml`) contendo a sua chave de acesso:
   ```env
   HUGGINGFACEHUB_API_TOKEN=hf_seu_token_real_aqui
   PORT=8000
   HOST=0.0.0.0
   ```
2. Execute o comando abaixo no terminal na raiz do projeto para construir as imagens e inicializar os serviços em segundo plano:
   ```bash
   docker compose up --build -d
   ```
3. Valide se todos os contêineres (`alura_agente_backend`, `alura_agente_frontend` e `alura_agente_proxy`) inicializaram com sucesso rodando:
   ```bash
   docker compose ps
   ```
4. Abra o seu navegador e acesse a aplicação unificada diretamente no endereço padrão HTTP: `http://localhost`

---

## 2. Roteiro Prático de Testes Baseado na Pasta Samples

Com os contêineres em execução, a interface carregará exibindo o indicador visual verde **"Backend Conectado"** no cabeçalho. Execute as seguintes validações de negócio:

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
1. Realize o upload do arquivo `dados_empresa.csv` na mesma área de arraste para mesclar os dados tabulares ao banco de vetores persistido no volume local.
2. Envie as perguntas estruturadas na caixa de chat:

*   **Pergunta 1:** `Qual é o preço do Notebook Pro 15 e quantas unidades temos em estoque?`
    *   **Resposta Esperada:** O preço é 4500.00 e o estoque possui 12 unidades.
*   **Pergunta 2:** `Onde fica a Cadeira Ergonômica e qual o valor dela?`
    *   **Resposta Esperada:** Fica localizada no Corredor B e custa 1200.00.
*   **Pergunta 3:** `Qual produto está localizado no Depósito Central e qual a quantidade dele em estoque?`
    *   **Resposta Esperada:** É a Mesa Digitalizadora, com 0 unidades em estoque.

### Cenário C: Teste de Blindagem Semântica contra Alucinações
Envie uma pergunta de escopo totalmente alheio aos documentos carregados para validar as diretivas de restrição do sistema:

*   **Pergunta:** `Como faço para assar um bolo de chocolate tradicional?`
    *   **Resposta Esperada:** O sistema deve recusar a geração e exibir estritamente o texto padrão de segurança configurado: `Desculpe, não encontrei essa informação nos documentos carregados.`
