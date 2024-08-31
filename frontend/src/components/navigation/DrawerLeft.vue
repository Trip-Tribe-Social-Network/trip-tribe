<template>
  <v-navigation-drawer :width="350" location="left" mobile-breakpoint="md">
    <v-card
      flat
      class="d-flex flex-column justify-center aligner-center text-center pa-2 mb-4"
    >
      <div class="d-flex flex-column justify-center align-center my-4">
        <v-avatar :image="user.avatar" size="100" class="mb-2" />
      </div>
      <h4>{{ user.name }}</h4>
    </v-card>
    <v-divider></v-divider>
    <v-card flat class="px-2">
      <v-list class="ma-3">
        <v-list-item
          to="/feed"
          class="text-body-2"
          prepend-icon="mdi-view-grid"
          color="pink-accent-3"
          >Feed
        </v-list-item>
        <v-list-item
          to="/chat"
          class="text-body-2"
          prepend-icon="mdi-comment-multiple"
          color="pink-accent-3"
          >Chat
        </v-list-item>
        <v-list-item
          :to="`/profile/${user.id}/friends`"
          class="text-body-2"
          prepend-icon="mdi-account-group"
          color="pink-accent-3"
          >Friends
        </v-list-item>
        <v-list-item
          :to="`/profile/${user.id}`"
          class="text-body-2"
          prepend-icon="mdi-account-circle"
          color="pink-accent-3"
          >Profile
        </v-list-item>
        <v-list-item
          class="text-body-2"
          prepend-icon="mdi-logout"
          color="pink-accent-3"
          @click="logout"
          >Logout
        </v-list-item>
      </v-list>
    </v-card>
    <v-divider></v-divider>
    <div class="text-body-2 my-2 px-4 pt-6">
      <div class="d-flex justify-start align-center px-4">
        <p class="font-weight-bold text-caption mr-2 text-uppercase">Conversations</p>
        <v-badge
          color="pink-accent-3"
          :content="store.conversations.length"
          inline
          class="flex-grow-1"
        ></v-badge>
      </div>
    </div>
    <v-card flat class="ma-3 pt-2">
      <v-list class="px-4">
        <div
          v-for="(conversation, index) in store.conversations.slice(0, 5)"
          :key="index"
          class="d-flex align-center py-1"
        >
          <v-avatar :image="userAvatar(conversation)" size="40" />
          <v-list-item class="text-body-2">{{ userName(conversation) }}</v-list-item>
          <v-spacer></v-spacer>
          <v-btn
            color="pink-accent-3"
            variant="text"
            size="small"
            @click="navigateToConversation(conversation.id)"
            icon="mdi-comment-multiple"
          />
        </div>
      </v-list>
    </v-card>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { User } from '@/models/user'
import { userUUID } from '@/utils/global'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'

const router = useRouter()
const store = useChatStore()
const userStore = useUserStore()

const user = computed((): User => userStore.user)
const avatarUrl = computed(() => user.value.avatar)

onMounted(() => store.getConversations())

const navigateToConversation = (conversationId: string) => {
  store.activeConversationId = conversationId
  router.push(`/conversation/${conversationId}`)
  store.getMessages(conversationId)
}

const userAvatar = (conversation: any) => {
  return conversation.users.filter((user: any) => user.id !== userUUID())[0].get_avatar
}

const userName = (conversation: any) => {
  return conversation.users.filter((user: any) => user.id !== userUUID())[0].name
}

const logout = () => userStore.logout()
</script>
