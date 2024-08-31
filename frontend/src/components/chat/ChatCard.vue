<template>
  <v-card class="ma-4 card" height="750" style="overflow-y: scroll">
    <v-card-actions class="d-flex bg-white">
      <v-btn icon="mdi-keyboard-backspace" to="/chat" />
    </v-card-actions>
    <v-divider></v-divider>
    <v-list
      data-testid="message"
      v-for="message in messages"
      :key="message.id"
      class="d-flex flex-column px-2 py-4"
      density="compact"
    >
      <v-list-item class="d-flex justify-center text-caption pb-4">
        {{ moment(message.created_at_formatted).format('lll') }}
      </v-list-item>
      <div
        class="d-flex justify-space-between pa-0"
        :class="[
          message.created_by.id === userUUID() ? 'justify-end' : 'justify-start',
          message.created_by.id === userUUID() ? 'flex-row-reverse' : 'flex-row'
        ]"
      >
        <div
          class="d-flex"
          :class="message.created_by.id === userUUID() ? 'flex-row-reverse' : 'flex-row'"
        >
          <v-avatar
            v-if="!smAndDown"
            :image="message.created_by.get_avatar"
            class="mx-2"
            size="40"
          ></v-avatar>
          <v-card
            variant="flat"
            density="compact"
            rounded
            shaped
            class="d-flex flex-column pa-3 text-justify"
            :color="
              message.created_by.id === userUUID() ? 'pink-lighten-1' : 'grey-lighten-2'
            "
          >
            <v-card-text
              density="compact"
              target="_blank"
              class="pa-0 text-caption"
              style="color: inherit"
            >
              {{ message.body }}
            </v-card-text>
          </v-card>
        </div>
      </div>
    </v-list>
  </v-card>
  <v-textarea
    v-model="body"
    data-testid="chat-input"
    class="ma-4"
    append-icon="mdi-send-variant-outline"
    type="text"
    variant="solo"
    hide-details
    rows="1"
    auto-grow
    clearable
    @click:append="handleSubmit"
  ></v-textarea>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import moment from 'moment'
import { useDisplay } from 'vuetify'
import { userUUID } from '@/utils/global'
import { useChatStore } from '@/stores/chat'
import type { Message } from '@/models/chat'

const { smAndDown } = useDisplay()
const store = useChatStore()
const body = ref('')

const handleSubmit = async () => {
  if (body.value.trim()) {
    await store.sendMessage(body.value)
    body.value = ''
  }
}
defineProps<{ messages: Message[] }>()
</script>

<style scoped>
.card {
  overflow-y: scroll;
  background-color: white;
}
</style>
