<template>
  <v-list
    v-for="request in filteredRequests"
    :key="request.id"
    lines="two"
    class="d-flex align-center"
  >
    <v-avatar
      data-testid="avatar"
      class="mr-3"
      :image="request.created_by.get_avatar"
      size="50"
    />
    <v-list-item :to="`/profile/${request.created_by.id}`">
      {{ request?.created_by.name }}
    </v-list-item>
    <v-spacer></v-spacer>
    <v-btn
      text="Accept"
      variant="flat"
      color="pink-accent-3"
      class="mr-3"
      @click="handleFriendshipRequest('accept', request.created_by.id)"
    />
    <v-btn
      text="Decline"
      variant="flat"
      color="pink-accent-3"
      @click="handleFriendshipRequest('reject', request.created_by.id)"
    />
  </v-list>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Request } from '@/models/friends'
import { useFriendsStore } from '@/stores/friends'
import { useUserStore } from '@/stores/user'
import type { Notification } from '@/models/global'

const store = useFriendsStore()
const userStore = useUserStore()
const requests = computed<Request[]>(() => store.requests)

const filteredRequests = computed(() =>
  requests.value.filter(request => request.status === 'sent')
)
const emit = defineEmits<(event: 'show-snackbar', payload: Notification) => void>()

const handleFriendshipRequest = async (status: 'accept' | 'reject', userId: string) => {
  await store
    .handleFriendRequest(status, userId)
    .then(() => {
      userStore.getBaseUser()
      emit('show-snackbar', {
        message: `Friend request updated successfully`,
        type: 'success'
      })
    })
    .catch(() => {
      emit('show-snackbar', {
        message: `Failed to update friend request`,
        type: 'error'
      })
    })
}
</script>
