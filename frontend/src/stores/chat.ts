import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'
import router from '@/router'
import type { Conversations, Conversation, Message } from '@/models/chat'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref<Conversations>([])
  const activeConversationId = ref<string | null>(null)
  const activeConversation = ref<Conversation | null>(null)
  const messages = ref<Message[]>([])
  const body = ref('')

  const getConversations = async (): Promise<Conversations> => {
    return new Promise((resolve, reject) => {
      axios
        .get('/api/chat/')
        .then(response => {
          conversations.value = response.data
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const getMessages = async (conversationID: string): Promise<Message[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/chat/${conversationID}/`)
        .then(response => {
          activeConversation.value = response.data
          messages.value = response.data.messages
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const sendDirectMessage = async (userUUID: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/chat/${userUUID}/get-or-create/`)
        .then(response => {
          router.push(`/conversation/${response.data.id}`)
          activeConversationId.value = response.data.id
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const sendMessage = async (message: string) => {
    if (!activeConversationId.value) {
      return
    }
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/chat/${activeConversationId.value}/send/`, {
          body: message
        })
        .then(response => {
          if (activeConversation.value) {
            activeConversation.value.messages.push(response.data)
          }
          getConversations()
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  return {
    conversations,
    messages,
    activeConversation,
    activeConversationId,
    body,
    getConversations,
    getMessages,
    sendMessage,
    sendDirectMessage
  }
})
