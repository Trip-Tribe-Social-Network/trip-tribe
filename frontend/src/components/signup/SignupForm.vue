<template>
  <v-form ref="form" @submit.prevent="signup()">
    <v-text-field
      v-model="email"
      label="Email"
      variant="outlined"
      class="mb-4"
      :rules="emailRules"
    />
    <v-text-field
      v-model="name"
      label="Username"
      variant="outlined"
      class="mb-4"
      :rules="usernameRules"
    />
    <v-text-field
      v-model="password1"
      label="Password"
      variant="outlined"
      :rules="passwordRules"
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      @click:append-inner="visible = !visible"
      class="mb-4"
    />
    <v-text-field
      v-model="password2"
      label="Confirm password"
      variant="outlined"
      :rules="passwordRules && confirmPasswordValidation"
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      @click:append-inner="visible = !visible"
      class="mb-4"
    />
    <v-card-actions class="pa-0 justify-end">
      <v-btn
        class="px-2"
        variant="flat"
        text="Sign up"
        color="pink-accent-3"
        type="submit"
        width="100%"
        size="large"
      />
    </v-card-actions>
  </v-form>
</template>

<script setup lang="ts">
import {
  emailRules,
  passwordRules,
  confirmPasswordRules,
  usernameRules
} from '@/utils/validationRules'
import router from '@/router'
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import type { VForm } from 'vuetify/components'
import type { SignupFormData } from '@/models/user'
import type { Notification } from '@/models/global'

const store = useUserStore()

const emit = defineEmits<{
  (event: 'show-snackbar', payload: Notification): void
}>()

const visible = ref<boolean>(false)
const email = ref<string>()
const name = ref<string>()
const password1 = ref<string>()
const password2 = ref<string>()
const form = ref<VForm | null>(null)

const confirmPasswordValidation = computed(() => {
  return confirmPasswordRules(password1.value || '')
})

const signup = async (): Promise<void> => {
  if (form.value) {
    const { valid } = await form.value.validate()
    if (valid) {
      const formData: SignupFormData = {
        email: email.value,
        name: name.value,
        password1: password1.value,
        password2: password2.value
      }
      store
        .signup(formData)
        .then(() => {
          emit('show-snackbar', {
            type: 'success',
            message: 'Signup successful!'
          })
          setTimeout(() => {
            router.push('/login')
          }, 1000)
        })
        .catch(() => {
          emit('show-snackbar', {
            type: 'error',
            message: 'Failed to signup'
          })
        })
    }
  }
}
</script>

<style scoped></style>
