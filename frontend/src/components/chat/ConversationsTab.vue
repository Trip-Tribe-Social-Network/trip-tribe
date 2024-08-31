<template>
  <v-list
    v-for="conversation in conversations"
    :key="conversation.id"
    class="d-flex align-center"
  >
    <v-avatar data-testid="user-avatar" :image="userAvatar(conversation)" />
    <v-list-item data-testid="user-name" class="text-body-2">
      {{ userName(conversation) }}
    </v-list-item>
    <v-spacer></v-spacer>
    <v-list-item-action>
      <v-btn
        text="Go"
        variant="flat"
        color="pink-accent-3"
        :to="`/conversation/${conversation.id}`"
      />
    </v-list-item-action>
  </v-list>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { userUUID } from '@/utils/global'
import { useChatStore } from '@/stores/chat'
import type { Conversations } from '@/models/chat'

const store = useChatStore()

const conversations = computed<Conversations>(() => store.conversations)

const userAvatar = (conversation: any) => {
  return conversation.users.filter((user: any) => user.id !== userUUID())[0].get_avatar
}

const userName = (conversation: any) => {
  return conversation.users.filter((user: any) => user.id !== userUUID())[0].name
}
</script>

<style scoped></style>
