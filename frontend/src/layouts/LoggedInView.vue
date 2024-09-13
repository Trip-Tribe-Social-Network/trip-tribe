<template>
  <v-layout>
    <AppToolbar />
    <DrawerLeft v-if="userIsAuthenticated" v-model="leftDrawer" />
    <DrawerRight v-model="rightDrawer" />
    <BottomNavigation v-if="bottomDrawer" />
    <v-main>
      <SearchComponent class="mx-4 mt-4" />
      <router-view />
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppToolbar from '@/components/navigation/AppToolbar.vue'
import BottomNavigation from '@/components/navigation/BottomNavigation.vue'
import SearchComponent from '@/components/SearchComponent.vue'
import DrawerLeft from '@/components/navigation/DrawerLeft.vue'
import DrawerRight from '@/components/navigation/DrawerRight.vue'

const store = useUserStore()
const userIsAuthenticated = computed<boolean>(() => store.user.isAuthenticated)

store.getBaseUser()
store.getNotifications()

const rightDrawer = ref(true)
const leftDrawer = ref(true)
const bottomDrawer = computed<boolean>(() => !leftDrawer.value && !rightDrawer.value)
</script>

<style scoped></style>
