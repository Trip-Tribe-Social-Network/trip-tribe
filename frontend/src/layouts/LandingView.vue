<template>
  <div id="home">
    <v-layout class="d-flex justify-center align-center">
      <v-app-bar class="px-6" flat>
        <div class="d-flex justify-center align-center flex-column">
          <v-img :src="logo" :width="40" class="text-center" />
        </div>
        <v-app-bar-title class="text-h5 font-weight-black title"
          >trip tribe</v-app-bar-title
        >
        <template v-slot:append>
          <v-btn @click="navigate('/login')" variant="outlined">Login</v-btn>
          <v-btn @click="navigate('/')" variant="text">Signup</v-btn>
        </template>
      </v-app-bar>
      <v-main
        class="d-flex align-center justify-center"
        style="min-height: 600px"
      >
        <router-view />
      </v-main>
    </v-layout>
  </div>
</template>

<script setup lang="ts">
import { navigate } from '@/utils/global'
import logo from '@/assets/logo.svg'
</script>

<style scoped>
#home {
  height: 100vh;
  background-color: white;
}

.title {
  font-family: 'Hind Vadodara', sans-serif;
}

.main {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
