<template>
  <v-alert
    :width="400"
    class="alert ma-3 text-center"
    v-if="isVisible"
    :color="alert.type === 'error' ? 'red' : 'green'"
    :type="alert.type"
  >
    {{ alert.message }}
  </v-alert>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Notification } from '@/models/global'

const props = defineProps<{
  alert: Notification
}>()

const isVisible = ref(false)

watch(
  () => props.alert,
  newAlert => {
    if (newAlert && newAlert.message) {
      isVisible.value = true
      setTimeout(() => {
        isVisible.value = false
      }, 2000)
    }
  },
  { immediate: true, deep: true }
)
</script>

<style scoped>
.alert {
  position: fixed;
  bottom: 0%;
  left: 50%;
  transform: translate(-50%);
}
</style>
