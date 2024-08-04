<template>
  <v-card
    :width="smAndDown ? '100%' : '50%'"
    class="d-flex justify-center align-center card"
    variant="flat"
  >
    <v-card variant="flat" width="90%">
      <p class="text-h3 text-center mb-4">Create Account</p>
      <v-card-text class="text-body-1 py-6 mb-4 px-0 text-justify content">
        Dive into a vibrant community of fellow explorers. Connect with
        like-minded emily who share your passion for exploration. Discover new
        destinations with recommendations and tips from those who’ve been there
        before. Your journey starts here. Embrace the world, one connection at a
        time!
      </v-card-text>
      <SignupForm @show-snackbar="showSnackbar" />
    </v-card>
  </v-card>
  <v-card
    v-if="!smAndDown"
    class="ma-8 card d-flex justify-center align-center rounded-lg"
    width="50%"
    height="800px"
  >
    <v-carousel :show-arrows="false" height="100%" hide-delimiter-background>
      <v-carousel-item
        v-for="(testimonial, index) in testimonials"
        :key="index"
      >
        <TestimonialComponent
          :image="testimonial.image"
          :name="testimonial.name"
          :location="testimonial.location"
          :quote="testimonial.quote"
        />
      </v-carousel-item>
    </v-carousel>
  </v-card>
  <AlertComponent :alert="appSnackbarConf" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useDisplay } from 'vuetify'
import type { Notification } from '@/models/global'
import AlertComponent from '@/components/AlertComponent.vue'
import SignupForm from '@/components/signup/SignupForm.vue'
import TestimonialComponent from '@/components/signup/TestimonialComponent.vue'
import emily from '@/assets/emily.jpeg'
import lukas from '@/assets/lukas.jpeg'
import sofia from '@/assets/sofia.jpeg'

const { smAndDown } = useDisplay()

const testimonials = [
  {
    image: emily,
    name: 'Emily Thompson',
    location: 'Dublin, Scotland',
    quote: `This social network has transformed my travel experiences. 
            I've made lifelong friends and discovered hidden gems worldwide. 
            It's a must-have for any traveler!`
  },
  {
    image: lukas,
    name: 'Lukas Müller',
    location: 'London, UK',
    quote: `This community has truly transformed my travel experiences. 
            It's connected me with fellow adventurers, helped me find 
            off-the-beaten-path spots, and provided a platform to share 
            my photography with a global audience.`
  },
  {
    image: sofia,
    name: 'Sofia Bianchi',
    location: 'Florence, Italy',
    quote: `As a 25-year-old traveler from Florence, this social network 
            has been a game-changer for me. I've reconnected with the joy 
            of discovery, met incredible people, and found hidden gems 
            across the globe.`
  }
]

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
