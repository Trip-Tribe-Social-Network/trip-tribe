import { ref } from 'vue'
import axios from 'axios'
import { defineStore } from 'pinia'
import type { UserFriends, User, Request } from '@/models/friends'

export const useFriendsStore = defineStore('friends', () => {
  const user = ref<User | null>(null)
  const friends = ref<User[]>([])
  const requests = ref<Request[]>([])

  const getFriends = async (userId: string): Promise<UserFriends> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/friends/${userId}/`)
        .then(response => {
          user.value = response.data.user
          friends.value = response.data.friends
          requests.value = response.data.requests
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const sendFriendRequest = (userId: string): Promise<{ message: string }> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/friends/${userId}/request/`)
        .then(response => {
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const handleFriendRequest = (
    status: 'accept' | 'reject',
    pk: string
  ): Promise<{ message: string }> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/friends/${pk}/${status}/`)
        .then(async response => {
          if (user.value) {
            await getFriends(user.value.id)
          }
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  return {
    getFriends,
    sendFriendRequest,
    handleFriendRequest,
    user,
    friends,
    requests
  }
})
