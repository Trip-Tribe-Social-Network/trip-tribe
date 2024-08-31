<template>
  <v-dialog max-width="500" v-if="user" persistent>
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        v-if="user.id === userUUID()"
        color="pink-accent-3"
        class="ma-4"
        data-testid="edit-profile"
        icon="mdi-pencil"
        rounded-xl
      ></v-btn>
    </template>
    <template v-slot:default>
      <v-card>
        <v-img height="150" :src="gradient" cover></v-img>
        <v-row justify="center">
          <v-col class="d-flex justify-center align-center" cols="12">
            <v-avatar :image="avatarUrl ?? user.get_avatar" size="180" class="profile" />
          </v-col>
        </v-row>
        <v-form ref="form" class="list ma-5">
          <v-text-field label="Name" v-model="user.name" />
          <v-text-field label="Email" v-model="user.email" />
          <v-text-field
            label="Bio"
            placeholder="bio"
            v-model="user.bio"
            :rules="counterRules"
            counter="45"
          ></v-text-field>
          <v-file-input
            accept="image/png, image/jpeg, image/jpg, image/bmp"
            prepend-icon="mdi-image"
            label="Avatar"
            @change="handleFileChange"
          />
          <v-card-actions class="d-flex justify-center ma-4">
            <v-spacer></v-spacer>
            <v-btn
              variant="outlined"
              data-testid="close-dialog"
              text="Close"
              @click="emit('close-dialog')"
              color="pink-accent-3"
            />
            <v-btn
              variant="flat"
              data-testid="save-changes"
              text="Save Changes"
              color="pink-accent-3"
              @click="editProfile"
            />
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { userUUID } from '@/utils/global'
import { counterRules } from '@/utils/validationRules'
import type { Notification } from '@/models/global'
import type { UserProfile } from '@/models/profile'
import { useProfileStore } from '@/stores/profile'
import { useUserStore } from '@/stores/user'
import type { VForm } from 'vuetify/components'
import gradient from '@/assets/gradient.jpeg'

const store = useProfileStore()
const userStore = useUserStore()
const user = computed((): UserProfile | undefined => store.user)
const form = ref<VForm | null>(null)
const avatar = ref<File | null>(null)
const avatarUrl = ref<string | null>(null)

const emit = defineEmits<{
  (event: 'show-snackbar', payload: Notification): void
  (event: 'close-dialog'): void
}>()

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files
  const file = files ? files[0] : null
  avatar.value = file
  if (file) {
    const reader = new FileReader()
    reader.onload = e => {
      avatarUrl.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const editProfile = async () => {
  if (user.value && form.value) {
    const { valid } = await form.value.validate()
    if (valid) {
      const formData = new FormData()
      formData.append('name', user.value.name)
      formData.append('email', user.value.email)
      formData.append('bio', user.value.bio)
      if (avatar.value) {
        formData.append('avatar', avatar.value)
      }
      store
        .editUserProfile(formData)
        .then(() => {
          userStore.getBaseUser()
          emit('show-snackbar', {
            type: 'success',
            message: 'Profile successfully updated'
          })
          emit('close-dialog')
        })
        .catch(() => {
          emit('show-snackbar', {
            type: 'error',
            message: 'Failed to update profile'
          })
        })
    }
  }
}
</script>

<style scoped>
.profile {
  border: 5px solid white;
  position: absolute;
  z-index: 100;
}

.list {
  padding-top: 120px;
}
</style>
