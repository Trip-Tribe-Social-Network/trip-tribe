<template>
  <v-alert
    :width="400"
    class="alert ma-3 text-center"
    v-if="alert && alert.type"
    :color="alert.type === 'error' ? 'red' : 'green'"
    :type="alert.type"
    :message="alert.message"
  >
    <p>{{ alert.message }}</p>
  </v-alert>
</template>

<script setup lang="ts">
import type { Notification } from '@/models/global'

defineProps<{
  alert: Notification
}>()
</script>

<style scoped>
.alert {
  position: fixed;
  bottom: 0%;
  left: 50%;
  transform: translate(-50%);
}
</style>
