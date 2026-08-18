<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { MessageSquare, Send, Loader2 } from 'lucide-vue-next';
import apiClient from '../../../shared/api/client';

defineProps<{ isDark: boolean }>();

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
  <div :class="[
    'border rounded-xl flex flex-col h-[calc(100vh-120px)] shadow-sm overflow-hidden transition-colors duration-300',
    isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
  ]">
    <div :class="[
      'px-4 py-3 border-b flex items-center space-x-2 transition-colors duration-300',
      isDark ? 'border-slate-800 bg-slate-950/20' : 'border-slate-200 bg-slate-50'
    ]">
      <div class="w-2 h-2 rounded-full bg-blue-500"></div>
      <h2 :class="['text-xs font-semibold uppercase tracking-wider', isDark ? 'text-slate-300' : 'text-slate-600']">Sessão Ativa do Chat</h2>
    </div>

    <div ref="scrollContainer" :class="[
      'flex-1 overflow-y-auto p-4 space-y-4 transition-colors duration-300',
      isDark ? 'bg-slate-950/10' : 'bg-slate-50/30'
    ]">
      <div v-if="messages.length === 0" class="h-full flex flex-col items-center justify-center text-center p-6 space-y-2">
        <MessageSquare :class="['w-6 h-6', isDark ? 'text-slate-600' : 'text-slate-300']" />
        <p :class="['text-xs font-medium', isDark ? 'text-slate-400' : 'text-slate-600']">O histórico de mensagens está vazio.</p>
        <p :class="['text-[11px] max-w-70', isDark ? 'text-slate-600' : 'text-slate-400']">Faça o upload de documentos e envie uma pergunta para iniciar o teste RAG.</p>
      </div>

      <div v-for="msg in messages" :key="msg.id" :class="['flex w-full', msg.sender === 'user' ? 'justify-end' : 'justify-start']">
        <div :class="[
          'max-w-[85%] rounded-xl px-4 py-3 text-xs leading-relaxed shadow-sm transition-all duration-200 whitespace-pre-wrap',
          msg.sender === 'user' 
            ? 'bg-blue-600 text-white rounded-br-none' 
            : (isDark ? 'bg-slate-800 text-slate-200 border border-slate-700/40 rounded-bl-none' : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none')
        ]">
          {{ msg.text }}
          <div :class="['text-[9px] mt-1 block text-right font-mono', msg.sender === 'user' ? 'text-blue-200' : 'text-slate-400']">
            {{ msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
          </div>
        </div>
      </div>

      <div v-if="isThinking" class="flex w-full justify-start animate-pulse">
        <div :class="[
          'rounded-xl rounded-bl-none px-4 py-3 text-xs flex items-center space-x-2 border transition-colors duration-300',
          isDark ? 'bg-slate-800 text-slate-400 border-slate-700/40' : 'bg-white text-slate-500 border-slate-200'
        ]">
          <Loader2 class="w-3.5 h-3.5 text-blue-500 animate-spin" />
          <span class="font-medium text-[11px]">Agente está processando a resposta...</span>
        </div>
      </div>
    </div>

    <div :class="[
      'p-4 border-t transition-colors duration-300',
      isDark ? 'border-slate-800 bg-slate-950/20' : 'border-slate-200 bg-slate-50'
    ]">
      <form @submit.prevent="sendMessage" class="flex items-center space-x-2">
        <input 
          type="text" 
          v-model="inputMessage" 
          placeholder="Digite sua dúvida com base nos documentos..." 
          :class="[
            'flex-1 border rounded-xl px-4 py-3 text-xs focus:outline-none focus:ring-1 transition-all duration-200',
            isDark 
              ? 'bg-slate-950 border-slate-800 text-slate-100 placeholder-slate-600 focus:border-blue-500 focus:ring-blue-500' 
              : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:border-blue-500 focus:ring-blue-500'
          ]"
          :disabled="isThinking"
        />
        <button 
          type="submit" 
          class="bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:hover:bg-blue-600 text-white font-medium text-xs px-5 py-3 rounded-xl transition-all duration-200 shadow-sm flex items-center space-x-1.5"
          :disabled="!inputMessage.trim() || isThinking"
        >
          <span>Enviar</span>
          <Send class="w-3 h-3" />
        </button>
      </form>
    </div>
  </div>
</template>
