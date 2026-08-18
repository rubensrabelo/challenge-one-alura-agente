<script setup lang="ts"></script>

<template>
  <div class="min-h-screen bg-neutral-900 text-neutral-100 flex flex-col font-sans">
    <header class="border-b border-neutral-800 bg-neutral-900/50 backdrop-blur px-6 py-4 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-orange-600 flex items-center justify-center font-bold text-white tracking-wider">A</div>
          <h1 class="text-lg font-semibold tracking-tight">Alura Agente <span class="text-xs text-neutral-500 font-mono">v2.4</span></h1>
        </div>
        <div class="flex items-center space-x-2 text-xs text-neutral-400 bg-neutral-800 px-3 py-1.5 rounded-full border border-neutral-700/50">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Backend Conectado</span>
        </div>
      </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <slot />
    </main>
  </div>
</template>
