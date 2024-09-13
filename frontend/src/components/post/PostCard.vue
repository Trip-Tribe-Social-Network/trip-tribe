<template>
  <v-card>
    <template v-slot:prepend>
      <div class="d-flex justify-space-between align-center pa-2">
        <v-avatar :image="post.created_by.get_avatar" size="50" class="mr-4" />
        <a
          class="text-body-2 text-black font-weight-bold text-decoration-none"
          :href="`/profile/${post.created_by.id}`"
        >
          {{ post.created_by.name }}
        </a>
      </div>
    </template>
    <template v-slot:append>
      <p class="text-body-2">
        {{ moment(post.created_at_formatted).format('ll') }}
      </p>
    </template>
    <div class="px-4">
      <div v-if="post.attachments.length">
        <v-img
          v-for="image in post.attachments"
          :src="image.get_image"
          class="py-2 px-4"
          max-height="350px"
          cover
        ></v-img>
      </div>
      <v-card-text v-if="post.body" class="text-body-2 text-justify px-1">
        {{ post.body }}
      </v-card-text>
    </div>
    <v-card-actions class="px-4 pt-0">
      <v-icon class="me-2" icon="mdi-heart-outline" @click="like"></v-icon>
      <span class="subheading me-4">{{ post.likes_count }}</span>
      <v-icon
        @click="toggleComments"
        class="me-2"
        icon="mdi-comment-multiple-outline"
      ></v-icon>
      <span class="subheading me-4">25</span>
      <v-spacer></v-spacer>
      <v-menu v-if="post.created_by.id === userUUID()">
        <template v-slot:activator="{ props }">
          <v-btn
            icon="mdi-dots-vertical"
            variant="text"
            size="small"
            v-bind="props"
          ></v-btn>
        </template>
        <v-list>
          <v-list-item
            base-color="red"
            prepend-icon="mdi-delete"
            @click="handleDeletePost"
            >Delete
          </v-list-item>
        </v-list>
      </v-menu>
    </v-card-actions>
    <v-list
      class="bg-grey-lighten-5"
      v-if="comments"
      height="200px"
      style="overflow-y: scroll"
    >
      <v-list-item>Item1</v-list-item>
      <v-list-item>Item2</v-list-item>
      <v-list-item>Item3</v-list-item>
      <v-list-item>Item4</v-list-item>
      <v-list-item>Item5</v-list-item>
    </v-list>
    <v-divider></v-divider>
    <v-card-actions class="px-4" v-if="comments">
      <v-text-field
        color="grey-lighten-2"
        density="compact"
        hide-details
        variant="outlined"
        append-inner-icon="mdi-send"
        outlined
      ></v-text-field>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import moment from 'moment'
import { userUUID } from '@/utils/global'
import type { Post } from '@/models/post'
import { usePostStore } from '@/stores/post'

const props = defineProps<{
  post: Post
}>()

const liked = ref(false)
const comments = ref(false)
const store = usePostStore()

const emit = defineEmits<(event: 'show-snackbar', payload: Notification) => void>()

const like = async () => {
  await store.likePost(props.post.id as string).then(() => {
    liked.value = true
  })
}

const handleDeletePost = async () => {
  await store.deletePost(props.post.id as string)
}
const toggleComments = () => {
  comments.value = !comments.value
}
</script>

<style scoped></style>
