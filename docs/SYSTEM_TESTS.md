# Guia de Execução e Homologação de Testes

Siga as instruções abaixo para subir os servidores locais e executar a homologação do pipeline RAG utilizando os arquivos de teste controlados.

## 1. Como Executar o Backend Localmente

### Pré-requisitos
* Python 3.10 ou superior.
* Token de Acesso de leitura válido da Hugging Face.

### Inicialização do Servidor
1. Navegue até o diretório do backend:
   ```bash
   cd app/backend
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie o arquivo `.env` dentro de `app/backend/` e configure suas variáveis:
   ```env
   HUGGINGFACEHUB_API_TOKEN=hf_seu_token_real_aqui
   PORT=8000
   HOST=0.0.0.0
   ```
5. Inicie o servidor FastAPI:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

---

## 2. Como Executar o Frontend Localmente

### Pré-requisitos
* Node.js LTS instalado (v18 ou superior).

### Inicialização da Interface
1. Abra uma nova aba do terminal na raiz do projeto e acesse o diretório correspondente:
   ```bash
   cd app/frontend
   ```
2. Instale os pacotes necessários:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento do Vite:
   ```bash
   npm run dev
   ```
4. Abra o navegador no endereço indicado: `http://localhost:5173/`

---

## 3. Roteiro Prático de Testes Baseado na Pasta Samples

Com as duas aplicações rodando, o indicador no cabeçalho exibirá a mensagem verde **"Backend Conectado"**. Execute as seguintes validações:

### Cenário A: Homologação do Arquivo PDF (`samples/diretrizes_suporte.pdf`)
1. Arraste o arquivo `diretrizes_suporte.pdf` para a área tracejada do componente de upload à esquerda.
2. Aguarde a mensagem de confirmação de indexação bem-sucedida.
3. Insira as seguintes perguntas no chat para validar as respostas com base no documento:

*   **Pergunta 1:** `Como funciona o horário de atendimento do suporte técnico para o plano Individual?`
    *   **Resposta Esperada:** Deve indicar que o atendimento ocorre de segunda a sexta-feira, das 08:00 às 18:00, via o e-mail suporte@aluraagente.com.br.
*   **Pergunta 2:** `Qual é o prazo para solicitar o reembolso total e quanto tempo demora o estorno no Pix?`
    *   **Resposta Esperada:** Deve citar o prazo estrito de até 7 dias corridos e o tempo de processamento de até 2 dias úteis para Pix.
*   **Pergunta 3:** `O suporte pode me pedir a senha ou token pelo WhatsApp em alguma situação?`
    *   **Resposta Esperada:** Deve declarar explicitamente que nenhum funcionário solicitará senhas ou tokens por aplicativos de mensagem.

### Cenário B: Homologação do Arquivo CSV (`samples/dados_empresa.csv`)
1. Realize o upload do arquivo `dados_empresa.csv` na mesma área de arraste para mesclar o banco vetorial local.
2. Envie as perguntas estruturadas na caixa de chat:

*   **Pergunta 1:** `Qual é o preço do Notebook Pro 15 e quantas unidades temos em estoque?`
    *   **Resposta Esperada:** O preço é 4500.00 e o estoque possui 12 unidades.
*   **Pergunta 2:** `Onde fica a Cadeira Ergonômica e qual o valor dela?`
    *   **Resposta Esperada:** Fica localizada no Corredor B e custa 1200.00.
*   **Pergunta 3:** `Qual produto está localizado no Depósito Central e qual a quantidade dele em estoque?`
    *   **Resposta Esperada:** É a Mesa Digitalizadora, com 0 unidades em estoque.

### Cenário C: Teste de Blindagem Semântica contra Alucinações
Envie uma pergunta de escopo totalmente alheio aos documentos para validar as diretivas de restrição do sistema:

*   **Pergunta:** `Como faço para assar um bolo de chocolate tradicional?`
    *   **Resposta Esperada:** O sistema deve exibir estritamente o texto padrão configurado: `Desculpe, não encontrei essa informação nos documentos carregados.`
