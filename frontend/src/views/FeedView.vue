<template>
  <div class="pa-4">
    <CreatePost />
    <div class="d-flex flex-column ga-8">
      <PostCard
        v-for="post in store.posts"
        :key="post.id"
        :post="post"
        @show-snackbar="showSnackbar"
      />
    </div>
    <AlertComponent :alert="appSnackbarConf" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { usePostStore } from '@/stores/post'
import PostCard from '@/components/post/PostCard.vue'
import CreatePost from '@/components/post/CreatePost.vue'
import AlertComponent from '@/components/AlertComponent.vue'

const store = usePostStore()
onMounted(() => store.fetchPosts())

const appSnackbarConf = ref<Notification>({
  message: '',
  type: undefined
})

const showSnackbar = (payload: Notification) => {
  appSnackbarConf.value.message = payload.message
  appSnackbarConf.value.type = payload.type
}
</script>

<style scoped></style>
