<script setup lang="ts">
import { ref } from 'vue';
import { UploadCloud, Loader2, AlertCircle, Check } from 'lucide-vue-next';
import apiClient from '../../../shared/api/client';

defineProps<{ isDark: boolean }>();

const isDragging = ref(false);
const isLoading = ref(false);
const message = ref<{ text: string; type: 'success' | 'error' } | null>(null);

const handleUpload = async (file: File) => {
  if (!file.name.endsWith('.pdf') && !file.name.endsWith('.csv')) {
    message.value = { text: 'Apenas arquivos .pdf ou .csv são permitidos.', type: 'error' };
    return;
  }

  isLoading.value = true;
  message.value = null;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await apiClient.post('/document/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    message.value = { text: response.data.message, type: 'success' };
  } catch (error: any) {
    const errorDetail = error.response?.data?.detail || 'Erro ao processar o documento no servidor.';
    message.value = { text: errorDetail, type: 'error' };
  } finally {
    isLoading.value = false;
  }
};

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files.length > 0) handleUpload(target.files[0]);
};

const onDrop = (e: DragEvent) => {
  isDragging.value = false;
  if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    handleUpload(e.dataTransfer.files[0]);
  }
};
</script>

<template>
  <div :class="[
    'border rounded-xl p-6 shadow-sm flex flex-col h-full justify-between transition-colors duration-300',
    isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
  ]">
    <div>
      <h2 :class="['text-sm font-medium mb-1', isDark ? 'text-slate-300' : 'text-slate-700']">Base de Conhecimento</h2>
      <p :class="['text-xs mb-4', isDark ? 'text-slate-500' : 'text-slate-400']">Adicione arquivos para alimentar o contexto do Agente Virtual.</p>
      
      <div 
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
        :class="[
          'border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-200 min-h-55',
          isDragging 
            ? 'border-blue-500 bg-blue-500/5' 
            : (isDark ? 'border-slate-800 hover:border-slate-700 bg-slate-950/40' : 'border-slate-200 hover:border-slate-300 bg-slate-50')
        ]"
        @click="($refs.fileInput as HTMLInputElement).click()"
      >
        <input type="file" ref="fileInput" class="hidden" accept=".pdf,.csv" @change="onFileChange" :disabled="isLoading" />
        
        <div v-if="isLoading" class="flex flex-col items-center space-y-3">
          <Loader2 class="w-8 h-8 text-blue-500 animate-spin" />
          <p :class="['text-xs font-medium', isDark ? 'text-slate-400' : 'text-slate-600']">Processando e indexando no FAISS...</p>
        </div>
        
        <div v-else class="space-y-2 flex flex-col items-center">
          <div :class="[
            'w-10 h-10 rounded-full flex items-center justify-center border transition-colors duration-300',
            isDark ? 'bg-slate-900 text-slate-400 border-slate-800' : 'bg-white text-slate-500 border-slate-200'
          ]">
            <UploadCloud class="w-5 h-5" />
          </div>
          <p :class="['text-xs font-medium', isDark ? 'text-slate-300' : 'text-slate-700']">Clique para buscar ou arraste o arquivo aqui</p>
          <p :class="['text-[10px]', isDark ? 'text-slate-500' : 'text-slate-400']">Suporta formatos PDF ou CSV estruturados</p>
        </div>
      </div>
    </div>

    <div class="mt-4 min-h-10">
      <div v-if="message" :class="[
        'p-3 rounded-lg text-xs font-medium border flex items-center space-x-2 transition-all duration-200', 
        message.type === 'success' 
          ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400' 
          : 'bg-rose-500/5 border-rose-500/20 text-rose-400'
      ]">
        <Check v-if="message.type === 'success'" class="w-4 h-4 shrink-0" />
        <AlertCircle v-else class="w-4 h-4 shrink-0" />
        <span>{{ message.text }}</span>
      </div>
    </div>
  </div>
</template>
