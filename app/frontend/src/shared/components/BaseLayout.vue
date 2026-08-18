<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { Sun, Moon, Cpu, CheckCircle, XCircle } from 'lucide-vue-next';
import apiClient from '../api/client';

const isDark = ref(true);
const isConnected = ref(false);
let checkInterval: ReturnType<typeof setInterval> | null = null;

const toggleTheme = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

const checkBackendHealth = async () => {
  try {
    const response = await apiClient.get('/');
    if (response.data && response.data.status === 'healthy') {
      isConnected.value = true;
    } else {
      isConnected.value = false;
    }
  } catch (error) {
    isConnected.value = false;
  }
};

onMounted(() => {
  document.documentElement.classList.add('dark');
  checkBackendHealth();
  checkInterval = setInterval(checkBackendHealth, 5000);
});

onUnmounted(() => {
  if (checkInterval) clearInterval(checkInterval);
});
</script>

<template>
  <div :class="[
    'min-h-screen flex flex-col font-sans transition-colors duration-300',
    isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'
  ]">
    <header :class="[
      'border-b px-6 py-4 sticky top-0 z-50 backdrop-blur transition-colors duration-300',
      isDark ? 'border-slate-800 bg-slate-950/70' : 'border-slate-200 bg-white/70'
    ]">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white tracking-wider">
            <Cpu class="w-4 h-4" />
          </div>
          <h1 class="text-lg font-semibold tracking-tight">
            Alura Agente <span :class="['text-xs font-mono', isDark ? 'text-slate-500' : 'text-slate-400']">v2.4</span>
          </h1>
        </div>
        
        <div class="flex items-center space-x-4">
          <button 
            @click="toggleTheme" 
            :class="[
              'p-2 rounded-lg border transition-all duration-200',
              isDark ? 'border-slate-800 bg-slate-900 text-amber-400 hover:bg-slate-800' : 'border-slate-200 bg-slate-100 text-blue-600 hover:bg-slate-200'
            ]"
            title="Alternar Tema"
          >
            <Sun v-if="isDark" class="w-4 h-4" />
            <Moon v-else class="w-4 h-4" />
          </button>

          <div :class="[
            'flex items-center space-x-2 text-xs px-3 py-1.5 rounded-full border transition-colors duration-300',
            isConnected 
              ? (isDark ? 'text-emerald-400 bg-emerald-950/20 border-emerald-900/30' : 'text-emerald-700 bg-emerald-50 border-emerald-200')
              : (isDark ? 'text-rose-400 bg-rose-950/20 border-rose-900/30' : 'text-rose-700 bg-rose-50 border-rose-200')
          ]">
            <CheckCircle v-if="isConnected" class="w-3.5 h-3.5 text-emerald-500" />
            <XCircle v-else class="w-3.5 h-3.5 text-rose-500 animate-pulse" />
            <span class="font-medium">{{ isConnected ? 'Backend Conectado' : 'Backend Desconectado' }}</span>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <slot :isDark="isDark" :isConnected="isConnected" />
    </main>
  </div>
</template>
