<template>
  <v-list :key="friend.id" v-for="friend in friends" class="d-flex align-center">
    <v-avatar data-testid="avatar" :image="friend.get_avatar" />
    <v-list-item>{{ friend.name }}</v-list-item>
    <v-spacer></v-spacer>
    <v-btn
      text="see profile"
      variant="flat"
      color="pink-accent-3"
      :to="`/profile/${friend.id}`"
    />
  </v-list>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { User } from '@/models/friends'
import { useFriendsStore } from '@/stores/friends'

const store = useFriendsStore()
const friends = computed<User[]>(() => store.friends)
</script>

<style scoped></style>
