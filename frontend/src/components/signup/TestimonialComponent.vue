<template>
  <v-sheet height="100%" tile class="gradient-overlay">
    <v-img :src="image" cover height="100%" class="rounded-lg" />
    <div class="d-flex flex-column justify-center align-center container">
      <div class="d-flex justify-center align-center">
        <v-chip
          class="mr-2 testimony"
          color="white"
          variant="outlined"
          size="large"
        >
          {{ name }}
        </v-chip>
        <v-chip class="testimony" color="white" variant="outlined" size="large">
          {{ location }}
        </v-chip>
      </div>
      <div
        class="d-flex justify-center text-h6 text-justify text-white font-weight-medium ma-8 testimony"
      >
        {{ quote }}
      </div>
    </div>
  </v-sheet>
</template>

<script setup lang="ts">
defineProps<{
  image: string
  name: string
  location: string
  quote: string
}>()
</script>

<style scoped>
.container {
  position: absolute;
  bottom: 70px;
  width: 100%;
}

.gradient-overlay {
  position: relative;
}

.gradient-overlay::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80%;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0));
  z-index: 100;
}

.gradient-overlay > .v-img {
  position: relative;
  z-index: 0;
}

.testimony {
  width: 80%;
  z-index: 200;
}
</style>
