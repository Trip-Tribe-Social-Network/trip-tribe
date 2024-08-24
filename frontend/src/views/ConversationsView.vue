<template>
  <v-card class="ma-4 pa-4">
    <v-tabs v-model="tab">
      <v-tab value="one" bg-color="transparent" color="pink-accent-3">
        Conversations ({{ store.conversations.length }})
      </v-tab>
    </v-tabs>
    <v-tabs-window v-model="tab">
      <v-tabs-window-item class="pa-4" value="one">
        <ConversationsTab />
      </v-tabs-window-item>
    </v-tabs-window>
  </v-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useChatStore } from '@/stores/chat'
import ConversationsTab from '@/components/chat/ConversationsTab.vue'

const tab = ref('one')
const store = useChatStore()

onMounted(() => {
  store.getConversations()
})
</script>

<style scoped></style>
