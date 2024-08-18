<template>
  <v-autocomplete
    :items="users"
    class="mx-auto"
    density="compact"
    type="search"
    v-model="searchTerm"
    item-title="name"
    @input="searchProfiles"
    prepend-inner-icon="mdi-magnify"
    style="max-width: 350px"
    variant="outlined"
    auto-select-first
    item-props
    hide-details
    hide-spin-buttons
    rounded
  >
    <template v-slot:item="{ props, item }">
      <v-list-item
        v-bind="props"
        :title="item.raw.name"
        :to="`/profile/${item.raw.id}`"
        :subtitle="item.raw.email"
        :prepend-avatar="item.raw.get_avatar || avatar"
      ></v-list-item>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import avatar from '@/assets/avatar.png'
import { useSearchStore } from '@/stores/search'
import type { UserProfile } from '@/models/profile'

const store = useSearchStore()
const searchTerm = ref('')
const users = computed((): UserProfile[] => store.users)

const searchProfiles = async () => {
  await store.search(searchTerm.value)
  searchTerm.value = ''
}
</script>

<style scoped>
.form {
  width: 40%;
}
.card {
  z-index: 100;
}
.autocomplete {
  z-index: 200;
  position: relative;
}
</style>
