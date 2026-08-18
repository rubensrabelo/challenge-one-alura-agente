<script setup lang="ts">
import BaseLayout from './shared/components/BaseLayout.vue';
import DocumentModule from './modules/document/views/DocumentModule.vue';
import ChatModule from './modules/chat/views/ChatModule.vue';
</script>

<template>
  <BaseLayout>
    <DocumentModule />
    <ChatModule />
  </BaseLayout>
</template>
