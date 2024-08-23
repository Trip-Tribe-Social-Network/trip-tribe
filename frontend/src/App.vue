<template>
  <LoggedInView v-if="store.user.isAuthenticated" />
  <LandingView v-else />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import LandingView from '@/layouts/LandingView.vue'
import LoggedInView from '@/layouts/LoggedInView.vue'

const store = useUserStore()

onMounted(() => {
  if (!store.user.isAuthenticated) {
    store.initializeStore()
  }
})
</script>

<style scoped></style>
