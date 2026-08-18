<script setup lang="ts">
import { ref } from 'vue';
import apiClient from '../../../shared/api/client';

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
  if (target.files && target.files[0]) handleUpload(target.files[0]);
};

const onDrop = (e: DragEvent) => {
  isDragging.value = false;
  if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
    handleUpload(e.dataTransfer.files[0]);
  }
};
</script>

<template>
  <div class="bg-neutral-900 border border-neutral-800 rounded-xl p-6 shadow-sm flex flex-col h-full justify-between">
    <div>
      <h2 class="text-sm font-medium text-neutral-300 mb-1">Base de Conhecimento</h2>
      <p class="text-xs text-neutral-500 mb-4">Adicione arquivos para alimentar o contexto do Agente Virtual.</p>
      
      <div 
        @dragover.prevent="isDragging = true"
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDrop"
        :class="[
          'border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-200 min-h-[220px]',
          isDragging ? 'border-orange-500 bg-orange-500/5' : 'border-neutral-800 hover:border-neutral-700 bg-neutral-950/40'
        ]"
        @click="($refs.fileInput as HTMLInputElement).click()"
      >
        <input type="file" ref="fileInput" class="hidden" accept=".pdf,.csv" @change="onFileChange" :disabled="isLoading" />
        
        <div v-if="isLoading" class="flex flex-col items-center space-y-3">
          <div class="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
          <p class="text-xs text-neutral-400 font-medium">Processando e indexando no FAISS...</p>
        </div>
        
        <div v-else class="space-y-2">
          <div class="mx-auto w-10 h-10 rounded-full bg-neutral-900 flex items-center justify-center text-neutral-400 border border-neutral-800">📥</div>
          <p class="text-xs font-medium text-neutral-300">Clique para buscar ou arraste o arquivo aqui</p>
          <p class="text-[10px] text-neutral-500">Suporta formatos PDF ou CSV estruturados</p>
        </div>
      </div>
    </div>

    <div class="mt-4 min-h-[40px]">
      <div v-if="message" :class="['p-3 rounded-lg text-xs font-medium border transition-all duration-200', message.type === 'success' ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400' : 'bg-rose-500/5 border-rose-500/20 text-rose-400']">
        {{ message.text }}
      </div>
    </div>
  </div>
</template>
