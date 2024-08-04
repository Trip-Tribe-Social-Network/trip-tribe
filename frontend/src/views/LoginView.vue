<template>
  <v-card
    :width="smAndDown ? '100%' : '50%'"
    class="d-flex justify-center align-center card"
    variant="flat"
  >
    <v-card variant="flat" width="90%" class="pa-4">
      <div class="d-flex justify-center align-center flex-column">
        <p class="text-h3 font-weight-medium">Log in</p>
      </div>
      <v-card-text class="text-body-1 py-8 px-0 text-justify content">
        Reconnect with your community of travelers and immerse yourself in the
        world of exploration once again. Share your latest adventures, whether
        you've scaled mountain peaks, wandered through ancient ruins, or
        discovered hidden gems in bustling cities. Your travel experiences and
        connections await, Welcome back!
      </v-card-text>
      <LoginForm @show-snackbar="showSnackbar" />
    </v-card>
  </v-card>
  <v-card
    v-if="!smAndDown"
    class="ma-8 card d-flex justify-center align-center rounded-lg"
    width="50%"
    height="800px"
  >
    <v-img :src="travelers" cover height="100%"></v-img>
  </v-card>
  <AlertComponent :alert="appSnackbarConf" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
import travelers from '@/assets/login-image.png'
import LoginForm from '@/components/login/LoginForm.vue'
import AlertComponent from '@/components/AlertComponent.vue'

const { smAndDown } = useDisplay()

const appSnackbarConf = ref<Notification>({
  message: '',
  type: undefined
})

const showSnackbar = (payload: Notification) => {
  appSnackbarConf.value.message = payload.message
  appSnackbarConf.value.type = payload.type
}
</script>

<style scoped>
.card {
  height: calc(100vh - 64px);
}

.content {
  line-height: 2;
}
</style>
