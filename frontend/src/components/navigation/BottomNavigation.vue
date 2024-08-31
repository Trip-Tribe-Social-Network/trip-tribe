<template>
  <v-bottom-navigation class="bottom-drawer">
    <v-btn
      to="/feed"
      class="text-caption"
      prepend-icon="mdi-view-grid"
      color="pink-accent-3"
    />
    <v-btn
      to="/chat"
      class="text-caption"
      prepend-icon="mdi-comment-multiple"
      color="pink-accent-3"
    />
    <v-btn
      :to="`/profile/${user.id}/friends`"
      class="text-caption"
      prepend-icon="mdi-account-group"
      color="pink-accent-3"
    />
    <v-btn
      :to="`/profile/${user.id}`"
      class="text-caption"
      prepend-icon="mdi-account"
      color="pink-accent-3"
    />
  </v-bottom-navigation>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { User } from '@/models/user'
import { useUserStore } from '@/stores/user'

const store = useUserStore()

const user = computed((): User => store.user)
</script>

<style scoped></style>
