# Alura Agente - Frontend Single Page Application (Vue 3 & TypeScript)

Esta camada compreende a interface de usuário (UI) reativa do sistema Alura Agente. A aplicação foi concebida sob o ecossistema moderno do Vite, utilizando arquitetura modular desacoplada e estilização utilitária de alta velocidade com Tailwind CSS v4.

## Tecnologias e Dependências Principais

*   **Vue 3 (Composition API)**: Framework progressivo focado em reatividade eficiente e estruturação via sintaxe simplificada `<script setup>`.
*   **TypeScript**: Tipagem estática rigorosa para prevenção de falhas em tempo de compilação.
*   **Tailwind CSS v4 (Oxide Engine)**: Motor compilado nativamente em Rust que elimina arquivos pesados de configuração (`tailwind.config.js`) e varre o código via CSS nativo (`@import "tailwindcss"`).
*   **Axios**: Cliente HTTP baseado em Promises para comunicação assíncrona com a API REST do backend.
*   **Lucide Vue Next**: Biblioteca de ícones vetoriais leves e consistentes substituindo inteiramente o uso de emojis.

---

## Estrutura de Arquivos (Módulos & Shared)

O código-fonte em `src/` adota o princípio de separação de responsabilidades globais e locais:

### Camada Shared (`src/shared/`)
Contém elementos transversais reaproveitados por toda a aplicação:
*   `api/client.ts`: Instância central do Axios configurada com o endereço base do servidor (`http://localhost:8000`).
*   `components/BaseLayout.vue`: Painel visual mestre que gerencia:
    1. A alternância dinâmica de tema (Escuro/Claro) adicionando/removendo a classe `.dark` da tag raiz do HTML.
    2. O monitoramento em tempo real (Polling via `setInterval` a cada 5 segundos) da integridade do backend, atualizando o componente visual de status.

### Camada Modules (`src/modules/`)
Isolamento dos contextos visuais por domínios de ação:
*   `document/`: Encapsula a lógica de arrastar e soltar (Drag and Drop) arquivos, monitorando estados de progresso de upload e exibindo notificações de sucesso ou falhas do servidor.
*   `chat/`: Gerencia a linha do tempo da conversa, controlando a injeção de novas bolhas de texto geradas pelo usuário ou agente, manipulando o scroll automático para o final da tela e bloqueando interações em caso de perda de sinal com a API.

---

## Padrão Visual e Comportamental

*   **Paleta de Cores**: Identidade baseada em tons sofisticados de azul e ardósia (`slate-950` para o fundo escuro e `white`/`slate-50` para o tema claro).
*   **Controles de Estados Reativos**: Toda a barra de digitação e os botões de disparo de mensagens são bloqueados de forma automática em dois cenários críticos:
    *   Enquanto a inteligência artificial está processando uma resposta anterior (`isThinking === true`).
    *   Caso a verificação em tempo real detecte a queda do backend (`isConnected === false`), alterando o marcador visual para vermelho.
