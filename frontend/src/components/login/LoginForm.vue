<template>
  <v-form ref="form" @submit.prevent="handleLogin()">
    <v-text-field
      v-model="email"
      label="Email"
      :rules="emailRules"
      variant="outlined"
      class="mb-4"
    />
    <v-text-field
      :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
      :type="visible ? 'text' : 'password'"
      @click:append-inner="visible = !visible"
      v-model="password"
      label="Password"
      variant="outlined"
      :rules="passwordRules"
      class="mb-4"
    />
    <v-card-actions class="pa-0 justify-end">
      <v-btn
        class="px-2"
        text="Login"
        data-testid="login-button"
        variant="flat"
        color="pink-accent-3"
        type="submit"
        width="100%"
        size="large"
      />
    </v-card-actions>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'
import { useUserStore } from '@/stores/user'
import type { VForm } from 'vuetify/components'
import type { Notification } from '@/models/global'
import type { LoginFormData } from '@/models/user'
import { emailRules, passwordRules } from '@/utils/validationRules'

const store = useUserStore()

const emit = defineEmits<{
  (event: 'show-snackbar', payload: Notification): void
}>()

const visible = ref<boolean>(false)
const email = ref<string>()
const password = ref<string>()
const form = ref<VForm | null>(null)

const handleLogin = async (): Promise<void> => {
  if (form.value) {
    const { valid } = await form.value.validate()
    if (valid) {
      const formData: LoginFormData = {
        email: email.value,
        password: password.value
      }
      store
        .login(formData)
        .then(() => {
          store.user.isAuthenticated = true
          setTimeout(() => {
            router.push('/feed')
          })
        })
        .catch(() => {
          emit('show-snackbar', {
            type: 'error',
            message: 'Failed to login'
          })
        })
    }
  }
}
</script>

<style scoped></style>
