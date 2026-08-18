<script setup lang="ts">
import FileUploader from '../components/FileUploader.vue';
defineProps<{ isDark: boolean }>();
</script>

<template>
  <div class="lg:col-span-4 h-fit lg:h-[calc(100vh-120px)]">
    <FileUploader :isDark="isDark" />
  </div>
</template>
