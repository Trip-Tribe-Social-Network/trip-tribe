<template>
  <v-layout>
    <AppToolbar />
    <DrawerLeft v-if="userIsAuthenticated" v-model="leftDrawer" :user="store.user" />
    <DrawerRight v-model="rightDrawer" />
    <v-bottom-navigation v-if="bottomDrawer" class="bottom-drawer">
      <v-btn
        to="/feed"
        class="text-caption"
        prepend-icon="mdi-view-grid"
        color="pink-accent-3"
      />
      <v-btn
        to="/chat"
        class="text-caption"
        prepend-icon="mdi-comment-multiple"
        color="pink-accent-3"
      />
      <v-btn
        :to="`/profile/${store.user.id}/friends`"
        class="text-caption"
        prepend-icon="mdi-account-group"
        color="pink-accent-3"
      />
      <v-btn
        :to="`/profile/${store.user.id}`"
        class="text-caption"
        prepend-icon="mdi-account"
        color="pink-accent-3"
      />
    </v-bottom-navigation>
    <v-main>
      <SearchComponent class="mx-4 mt-4" />
      <router-view />
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { computed, ref } from 'vue'
import { RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import AppToolbar from '@/components/AppToolbar.vue'
import SearchComponent from '@/components/SearchComponent.vue'
import DrawerLeft from '@/components/navigation/DrawerLeft.vue'
import DrawerRight from '@/components/navigation/DrawerRight.vue'

const store = useUserStore()
const userIsAuthenticated = computed(() => store.user.isAuthenticated)

onMounted(() => {
  store.getBaseUser()
})

const rightDrawer = ref(true)
const leftDrawer = ref(true)
const bottomDrawer = computed(() => !leftDrawer.value && !rightDrawer.value)
</script>

<style scoped></style>
