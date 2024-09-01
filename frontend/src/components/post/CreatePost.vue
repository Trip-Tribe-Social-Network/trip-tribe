<template>
  <v-card class="d-flex flex-column justify-center pa-2 mb-6">
    <v-form ref="form">
      <v-textarea
        v-model="postContent"
        bg-color="grey-lighten-4"
        hide-details
        auto-grow
        clearable
        outlined
        rows="5"
        class="mx-4 mt-4 text-justify"
      ></v-textarea>
      <v-card-actions class="pa-4">
        <v-file-input
          v-model="image"
          variant="outlined"
          color="pink-accent-3"
          density="compact"
          accept="image/png, image/jpeg, image/jpg, image/bmp"
          prepend-icon="mdi-image"
          hide-details
        />
        <v-spacer></v-spacer>
        <v-btn
          text="Create a Post"
          variant="flat"
          color="pink-accent-3"
          @click="handleCreatePost"
        />
      </v-card-actions>
    </v-form>
    <v-spacer></v-spacer>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { usePostStore } from '@/stores/post'

const store = usePostStore()

const postContent = ref('')
const image = ref<File | null>(null)
const form = ref<HTMLFormElement | null>(null)

const handleCreatePost = () => {
  if (form.value) {
    const formData = new FormData()
    formData.append('body', postContent.value)
    if (image.value) {
      formData.append('image', image.value)
    }

    store.createPost(formData).then(() => {
      postContent.value = ''
      image.value = null
    })
  }
}
</script>

<style scoped>
.textarea {
  overflow: hidden;
  max-height: 100px;
}
</style>
