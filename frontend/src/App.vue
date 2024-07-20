<template>
  <LoggedInView v-if="userIsAuthenticated" />
  <LandingView v-else />
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import LoggedInView from '@/layouts/LoggedInView.vue'
import LandingView from './layouts/LandingView.vue'
import { useUserStore } from '@/stores/user'

const store = useUserStore()

const userIsAuthenticated = computed(() => store.user.isAuthenticated)

onMounted(() => {
  store.initializeStore()
})
</script>

<style scoped></style>
