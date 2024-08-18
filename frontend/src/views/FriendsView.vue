<template>
  <v-card class="ma-4 pa-4">
    <v-tabs v-model="tab" bg-color="transparent" color="pink-accent-3">
      <v-tab value="one">Friends ({{ store.friends.length }})</v-tab>
      <v-tab value="two">Requests ({{ sentRequestsCount }})</v-tab>
    </v-tabs>
    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="one">
          <FriendsCard />
        </v-tabs-window-item>
        <v-tabs-window-item value="two">
          <FriendsRequest @show-snackbar="showSnackbar" />
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
  <AlertComponent :alert="appSnackbarConf" />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { userUUID } from '@/utils/global'
import type { Notification } from '@/models/global'
import { useFriendsStore } from '@/stores/friends'
import FriendsCard from '@/components/friends/FriendsCard.vue'
import FriendsRequest from '@/components/friends/FriendsRequest.vue'
import AlertComponent from '@/components/AlertComponent.vue'

const tab = ref('one')
const store = useFriendsStore()

store.getFriends(userUUID() as string)

const appSnackbarConf = ref<Notification>({
  message: '',
  type: undefined
})

const showSnackbar = (payload: Notification) => {
  appSnackbarConf.value = payload
}

const sentRequestsCount = computed(() => {
  return store.requests.filter(request => request.status === 'sent').length
})
</script>

<style scoped></style>
