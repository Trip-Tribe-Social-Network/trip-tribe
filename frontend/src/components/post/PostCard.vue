<template>
  <v-card>
    <template v-slot:prepend>
      <div class="d-flex justify-space-between align-center pa-2">
        <v-avatar :image="post.created_by.get_avatar || avatar" size="50" class="mr-4" />
        <p class="text-body-2 font-weight-bold">{{ post.created_by.name }}</p>
      </div>
    </template>
    <template v-slot:append>
      <p class="text-body-2">{{ post.created_at_formatted }} ago</p>
    </template>
    <div class="px-4">
      <v-img
        :src="lagoon"
        class="py-2 px-4"
        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
        max-height="300px"
        cover
      ></v-img>
      <v-card-text v-if="post.body" class="text-body-2 text-justify px-1">
        {{ post.body }}
      </v-card-text>
    </div>
    <v-card-actions class="px-4 pt-0">
      <v-icon
        class="me-2"
        :icon="liked ? 'mdi-heart' : 'mdi-heart-outline'"
        :color="liked ? 'red' : 'black'"
        @click="like"
      ></v-icon>
      <span class="subheading me-4">{{ post.likes_count }}</span>
      <v-icon
        @click="toggleComments"
        class="me-2"
        icon="mdi-comment-multiple-outline"
      ></v-icon>
      <span class="subheading me-4">25</span>

      <v-spacer></v-spacer>
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn
            icon="mdi-dots-vertical"
            variant="text"
            size="small"
            v-bind="props"
          ></v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item prepend-icon="mdi-delete">Delete Post</v-list-item>
            <v-list-item>Report Post</v-list-item>
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
import avatar from '@/assets/avatar.png'
import lagoon from '@/assets/lagoon.jpeg'
import type { Post } from '@/models/post'
import { usePostStore } from '@/stores/post'
import { ref } from 'vue'

const props = defineProps<{
  post: Post
}>()

const store = usePostStore()
const comments = ref(false)
const liked = ref(false)

const emit = defineEmits<{
  (event: 'show-snackbar', payload: Notification): void
}>()

const like = async () => {
  await store
    .likePost(props.post.id as string)
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
const toggleComments = () => {
  comments.value = !comments.value
}
</script>

<style scoped></style>
