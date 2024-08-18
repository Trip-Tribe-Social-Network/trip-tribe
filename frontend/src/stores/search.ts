import { ref } from 'vue'
import axios from 'axios'
import { defineStore } from 'pinia'
import type { UserProfile } from '@/models/profile'

export const useSearchStore = defineStore('search', () => {
  const users = ref<UserProfile[]>([])

  const search = (query: string): Promise<UserProfile[]> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/search/`, { query: query })
        .then(response => {
          users.value = response.data.users
          resolve(response.data)
        })
        .catch(error => reject(error))
    })
  }

  return {
    search,
    users
  }
})
