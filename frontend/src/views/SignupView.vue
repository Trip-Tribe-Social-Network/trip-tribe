<template>
  <v-card
    v-if="!smAndDown"
    variant="flat"
    width="50%"
    class="pa-8 card d-flex justify-center align-center"
  >
    <v-img :src="travelers" cover height="100%" class="rounded-xl" />
  </v-card>
  <v-card
    :width="smAndDown ? '100%' : '50%'"
    class="d-flex justify-center align-center card"
    variant="flat"
  >
    <v-card variant="flat" width="80%">
      <div class="d-flex justify-center align-center flex-column">
        <v-img :src="logo" :width="80" class="text-center" />
      </div>
      <v-card-title class="text-center text-h4 font-weight-bold">
        Create Account
      </v-card-title>
      <v-card-text class="text-body-1 py-6 px-0 text-justify">
        Dive into a vibrant community of fellow explorers. Connect with
        like-minded travelers who share your passion for exploration. Discover
        new destinations with recommendations and tips from those who’ve been
        there before.Your journey starts here. Embrace the world, one connection
        at a time!
      </v-card-text>
      <SignupForm @show-snackbar="showSnackbar" />
    </v-card>
  </v-card>
  <AlertComponent :alert="appSnackbarConf" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import logo from '@/assets/logo.svg'
import travelers from '@/assets/travelers-2.jpg'
import { useDisplay } from 'vuetify'
import type { Notification } from '@/models/global'
import AlertComponent from '@/components/AlertComponent.vue'
import SignupForm from '@/components/signup/SignupForm.vue'

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

.text {
  line-height: 2;
}
</style>
