<template>
  <v-card flat class="ma-3">
    <v-card-title class="text-body-2 my-2">
      <div class="d-flex align-center">
        <p class="font-weight-bold text-caption mr-2 text-uppercase">Trends</p>
        <v-icon color="pink-accent-3" icon="mdi-trending-up"></v-icon>
      </div>
    </v-card-title>
    <v-list>
      <v-list-item v-for="(trend, index) in store.trends.slice(0, 6)">
        <template v-slot:append>
          <v-btn
            text="Explore"
            variant="tonal"
            color="pink-accent-3"
            size="small"
            :to="`/trends/${trend.hashtag.toLowerCase()}`"
          />
        </template>
        <template v-slot:prepend>
          <p color=" pink-accent-3" class="text-body-2 text-truncate">
            # {{ trend.hashtag }}
          </p>
        </template>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { usePostStore } from '@/stores/post'

const store = usePostStore()

store.getTrends()
</script>
