<template>
  <div id="home">
    <v-layout class="d-flex justify-center align-center">
      <v-app-bar class="px-8 py-2" flat>
        <div class="d-flex justify-center align-center flex-column">
          <v-img :src="logo" :width="150" class="text-center ma-4" />
        </div>
        <template v-slot:append>
          <v-btn
            to="/"
            text="Login"
            variant="text"
            class="mr-4"
            color="pink-accent-3"
          />
          <v-btn
            to="/signup"
            text="Create an account"
            variant="flat"
            color="pink-accent-3"
          />
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
import logo from '@/assets/logo.png'
</script>

<style scoped>
#home {
  height: 100vh;
  background-color: white;
}

body {
  overflow-y: scroll;
}

.main {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
