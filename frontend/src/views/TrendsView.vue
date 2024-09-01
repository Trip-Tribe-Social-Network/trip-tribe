<template>
  <div class="pa-4">
    <CreatePost />
    <div class="d-flex flex-column ga-8">
      <PostCard v-for="post in store.posts" :key="post.id" :post="post" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { onMounted, watch } from 'vue'
import { usePostStore } from '@/stores/post'
import PostCard from '@/components/post/PostCard.vue'
import CreatePost from '@/components/post/CreatePost.vue'

const route = useRoute()
const store = usePostStore()

store.getTrendPosts(route.params.id as string)

watch(
  () => route.params.id,
  newId => {
    store.getTrendPosts(newId as string)
  }
)
</script>

<style scoped></style>
