<template>
  <v-app-bar class="app-bar px-4" flat>
    <template v-slot:prepend>
      <v-img :src="logo" width="100" />
    </template>
    <template v-slot:append>
      <div class="d-flex align-center ga-6">
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" class="text-none" stacked>
              <v-badge color="pink-accent-3" :content="notifications.length">
                <v-icon>mdi-earth</v-icon>
              </v-badge>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-if="notifications.length > 0"
              v-for="(notification, index) in notifications"
              class="d-flex"
              :key="notification.id"
            >
              <v-list-item-title>{{ notification.body }}</v-list-item-title>
            </v-list-item>
            <v-list-item v-else>
              <v-list-item-title>You don't have notifications</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-avatar :image="user.avatar" v-bind="props" class="rounded-0"></v-avatar>
          </template>
          <v-list>
            <v-list-item
              to="/feed"
              title="Feed"
              prepend-icon="mdi-view-grid"
              color="pink-accent-3"
            />
            <v-list-item
              to="/chat"
              title="Chat"
              prepend-icon="mdi-comment-multiple"
              color="pink-accent-3"
            />
            <v-list-item
              :to="`/profile/${user.id}/friends`"
              title="Friends"
              prepend-icon="mdi-account-group"
              color="pink-accent-3"
            />
            <v-list-item
              :to="`/profile/${user.id}`"
              title="Profile"
              prepend-icon="mdi-account-circle"
              color="pink-accent-3"
            />
            <v-list-item title="Logout" prepend-icon="mdi-logout" @click="logout" />
          </v-list>
        </v-menu>
      </div>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import logo from '@/assets/logo.png'
import { useUserStore } from '@/stores/user'
import type { User, Notification } from '@/models/user'

const store = useUserStore()
const logout = () => store.logout()
const user = computed<User>(() => store.user)
const notifications = computed<Notification[]>(() => store.notifications)
</script>

<style scoped>
.app-bar {
  border-bottom: 1px solid #e0e0e0;
}
</style>
