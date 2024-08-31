<template>
  <v-navigation-drawer :width="350" location="right" v-model="rightDrawer">
    <v-card flat class="ma-3">
      <v-card-title class="text-body-2 my-2">
        <div class="d-flex justify-start align-center w-100">
          <p class="font-weight-bold text-caption mr-2 text-uppercase">Friends</p>
          <v-badge color="pink-accent-3" :content="user.friends.length" inline></v-badge>
        </div>
      </v-card-title>
      <v-list class="pr-4">
        <div
          v-for="(friend, index) in user.friends.slice(0, 5)"
          :key="index"
          class="d-flex align-center py-1"
        >
          <v-list-item :prepend-avatar="friend.get_avatar" class="text-body-2">
            {{ friend.name }}
          </v-list-item>
          <v-spacer></v-spacer>
          <v-btn
            text="Profile"
            color="pink-accent-3"
            variant="tonal"
            size="small"
            :to="`/profile/${friend.id}`"
          ></v-btn>
        </div>
      </v-list>
    </v-card>
    <v-divider></v-divider>
    <TrendsCard />
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import TrendsCard from '@/components/post/TrendsCard.vue'
import type { User } from '@/models/user'
import { useUserStore } from '@/stores/user'
import { usePostStore } from '@/stores/post'
import { ref, computed } from 'vue'

const store = useUserStore()
const rightDrawer = ref(true)
const user = computed((): User => store.user)
</script>

<style lang="scss" scoped></style>
