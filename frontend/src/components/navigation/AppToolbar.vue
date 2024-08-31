<template>
  <v-app-bar class="app-bar px-4" flat>
    <template v-slot:prepend>
      <v-img :src="logo" width="100" />
    </template>
    <template v-slot:append>
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-avatar :image="user.avatar" v-bind="props" class="rounded-0"></v-avatar>
        </template>
        <v-list>
          <v-list-item>
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
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import logo from '@/assets/logo.png'
import type { User } from '@/models/user'
import { useUserStore } from '@/stores/user'

const store = useUserStore()
const logout = () => store.logout()
const user = computed((): User => store.user)
</script>

<style scoped>
.app-bar {
  border-bottom: 1px solid #e0e0e0;
}
</style>
