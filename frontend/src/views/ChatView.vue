<template>
  <ChatCard :messages="store.messages" />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import ChatCard from '@/components/chat/ChatCard.vue'

const route = useRoute()
const store = useChatStore()

onMounted(() => {
  store.getMessages(route.params.id as string)
})
</script>

<style scoped></style>
