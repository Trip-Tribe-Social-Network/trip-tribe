import { ref } from 'vue'
import axios from 'axios'
import { defineStore } from 'pinia'
import type { Post } from '@/models/post'
import type { Profile, UserProfile } from '@/models/profile'

export const useProfileStore = defineStore('profile', () => {
  const posts = ref<Post[]>([])
  const user = ref<UserProfile>()

  const getFeed = (userId: string): Promise<Profile> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/posts/profile/${userId}/`)
        .then(response => {
          user.value = response.data.user
          posts.value = response.data.posts
          resolve(response.data)
        })
        .catch(error => reject(error))
    })
  }

  const editUserProfile = async (formData: FormData): Promise<UserProfile> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/edit_profile/`, formData)
        .then(async response => {
          if (user.value) {
            await getFeed(user.value.id)
          }
          resolve(response.data)
        })
        .catch(error => reject(error))
    })
  }

  return {
    posts,
    user,
    getFeed,
    editUserProfile
  }
})
