<template>
  <v-card class="mb-2">
    <v-img height="130" :src="gradient" cover>
      <ProfileEdit
        v-model="isDialogVisible"
        @show-snackbar="handleShowSnackbar"
        @close-dialog="handleCloseDialog"
      />
    </v-img>
    <v-row justify="center">
      <v-col class="d-flex justify-center align-center" cols="12">
        <v-avatar
          :image="user?.get_avatar"
          data-testid="avatar"
          alt="Avatar"
          size="180"
          class="profile"
        />
      </v-col>
    </v-row>
    <div class="list pb-3">
      <v-list>
        <v-list-item-title class="d-flex justify-center font-weight-bold pb-4">
          {{ user?.name }}
        </v-list-item-title>
        <v-list-item
          v-if="user?.bio"
          class="text-grey-darken-2 text-body-2 pa-4 d-flex justify-center"
        >
          {{ user.bio }}
        </v-list-item>
      </v-list>
      <v-list class="d-flex justify-center">
        <v-list-item>
          <div class="d-flex flex-column justify-center align-center">
            <p class="font-weight-bold">{{ user.friends?.length || 0 }}</p>
            <p class="text-caption">Friends</p>
          </div>
        </v-list-item>
        <v-list-item>
          <div class="d-flex flex-column justify-center align-center">
            <p class="font-weight-bold">{{ posts?.length || 0 }}</p>
            <p class="text-caption">Posts</p>
          </div>
        </v-list-item>
      </v-list>
    </div>
    <v-card-actions class="d-flex justify-center mx-4 mb-4" v-if="user.id !== userUUID()">
      <v-spacer></v-spacer>
      <v-btn
        v-if="user.id !== userUUID()"
        variant="flat"
        text="Direct Message"
        color="pink-accent-3"
        @click="sendFriendMessage"
      />
      <v-btn
        v-if="isRequestButtonVisible"
        variant="flat"
        text="Send request"
        color="pink-accent-3"
        @click="sendFriendRequest"
      />
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import ProfileEdit from '@/components/profile/ProfileEdit.vue'
import type { UserProfile } from '@/models/profile'
import type { Notification } from '@/models/global'
import type { Post } from '@/models/post'
import { useFriendsStore } from '@/stores/friends'
import { useChatStore } from '@/stores/chat'
import gradient from '@/assets/gradient.jpeg'
import { useRoute } from 'vue-router'
import { userUUID } from '@/utils/global'

const props = defineProps<{
  posts: Post[]
  user: UserProfile
}>()

const route = useRoute()
const store = useFriendsStore()
const chatStore = useChatStore()
const isDialogVisible = ref(false)

const emit = defineEmits<{
  (event: 'show-snackbar', payload: Notification): void
}>()

const handleShowSnackbar = (payload: Notification) => {
  emit('show-snackbar', payload)
}

const handleCloseDialog = () => {
  isDialogVisible.value = false
}

const isRequestButtonVisible = computed(() => {
  return (
    props.user.id !== userUUID() &&
    !props.user.friends.some(friend => friend === userUUID())
  )
})

const sendFriendRequest = async () => {
  await store
    .sendFriendRequest(route.params.id as string)
    .then(response => {
      emit('show-snackbar', {
        type: 'success',
        message: response.message
      })
    })
    .catch(error => {
      emit('show-snackbar', {
        type: 'error',
        message: error.message
      })
    })
}

const sendFriendMessage = async () => {
  await chatStore.sendDirectMessage(route.params.id as string)
}
</script>

<style scoped>
.profile {
  border: 5px solid white;
  position: absolute;
  z-index: 100;
}

.list {
  padding-top: 100px;
}
</style>
