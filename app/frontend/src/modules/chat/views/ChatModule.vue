<script setup lang="ts">
import ChatWindow from '../components/ChatWindow.vue';
defineProps<{ isDark: boolean }>();
</script>

<template>
  <div class="lg:col-span-8">
    <ChatWindow :isDark="isDark" />
  </div>
</template>
