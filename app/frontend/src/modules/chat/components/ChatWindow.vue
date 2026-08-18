<script setup lang="ts">
import { ref, nextTick } from 'vue';
import apiClient from '../../../shared/api/client';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: Date;
}

const messages = ref<Message[]>([]);
const inputMessage = ref('');
const isThinking = ref(false);
const scrollContainer = ref<HTMLDivElement | null>(null);

const scrollToBottom = async () => {
  await nextTick();
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isThinking.value) return;

  const userPrompt = inputMessage.value.trim();
  inputMessage.value = '';
  
  messages.value.push({
    id: crypto.randomUUID(),
    text: userPrompt,
    sender: 'user',
    timestamp: new Date()
  });
  
  await scrollToBottom();
  isThinking.value = true;

  try {
    const response = await apiClient.post('/chat/ask', { question: userPrompt });
    messages.value.push({
      id: crypto.randomUUID(),
      text: response.data.answer,
      sender: 'agent',
      timestamp: new Date()
    });
  } catch (error: any) {
    const detail = error.response?.data?.detail || 'Erro ao estabelecer comunicação com o agente.';
    messages.value.push({
      id: crypto.randomUUID(),
      text: `Falha na requisição: ${detail}`,
      sender: 'agent',
      timestamp: new Date()
    });
  } finally {
    isThinking.value = false;
    await scrollToBottom();
  }
};
</script>

<template>
  <div class="bg-neutral-900 border border-neutral-800 rounded-xl flex flex-col h-[calc(100vh-120px)] shadow-sm overflow-hidden">
    <div class="px-4 py-3 border-b border-neutral-800 bg-neutral-950/20 flex items-center space-x-2">
      <div class="w-2 h-2 rounded-full bg-orange-500"></div>
      <h2 class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">Sessão Ativa do Chat</h2>
    </div>

    <div ref="scrollContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-neutral-950/10">
      <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-center p-6 space-y-2">
        <div class="text-2xl">🤖</div>
        <p class="text-xs font-medium text-neutral-400">O histórico de mensagens está vazio.</p>
        <p class="text-[11px] text-neutral-600 max-w-[280px]">Faça o upload de documentos e envie uma pergunta para iniciar o teste RAG.</p>
      </div>

      <div v-for="msg in messages" :key="msg.id" :class="['flex w-full', msg.sender === 'user' ? 'justify-end' : 'justify-start']">
        <div :class="[
          'max-w-[85%] rounded-xl px-4 py-3 text-xs leading-relaxed shadow-sm transition-all duration-200 whitespace-pre-wrap',
          msg.sender === 'user' ? 'bg-orange-600 text-white rounded-br-none' : 'bg-neutral-800 text-neutral-200 border border-neutral-700/40 rounded-bl-none'
        ]">
          {{ msg.text }}
          <div :class="['text-[9px] mt-1 block text-right font-mono', msg.sender === 'user' ? 'text-orange-200' : 'text-neutral-500']">
            {{ msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
          </div>
        </div>
      </div>

      <div v-if="isThinking" class="flex w-full justify-start animate-pulse">
        <div class="bg-neutral-800 text-neutral-400 border border-neutral-700/40 rounded-xl rounded-bl-none px-4 py-3 text-xs flex items-center space-x-2">
          <div class="flex space-x-1">
            <div class="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
            <div class="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
            <div class="w-1.5 h-1.5 bg-neutral-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
          </div>
          <span class="font-medium text-[11px]">Agente está processando a resposta...</span>
        </div>
      </div>
    </div>

    <div class="p-4 border-t border-neutral-800 bg-neutral-950/20">
      <form @submit.prevent="sendMessage" class="flex items-center space-x-2">
        <input 
          type="text" 
          v-model="inputMessage" 
          placeholder="Digite sua dúvida com base nos documentos..." 
          class="flex-1 bg-neutral-950 border border-neutral-800 rounded-xl px-4 py-3 text-xs text-neutral-100 placeholder-neutral-600 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all duration-200"
          :disabled="isThinking"
        />
        <button 
          type="submit" 
          class="bg-orange-600 hover:bg-orange-500 disabled:opacity-40 disabled:hover:bg-orange-600 text-white font-medium text-xs px-5 py-3 rounded-xl transition-all duration-200 shadow-sm flex items-center justify-center"
          :disabled="!inputMessage.trim() || isThinking"
        >
          Enviar
        </button>
      </form>
    </div>
  </div>
</template>
