import { defineStore } from 'pinia'
import type { User, TokenData, SignupFormData } from '@/models/user'
import axios from 'axios'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({
    isAuthenticated: false,
    id: null,
    name: null,
    email: null,
    access: null,
    refresh: null
  })

  const initializeStore = (): void => {
    if (localStorage.getItem('user.access')) {
      user.value.isAuthenticated = true
      user.value.id = localStorage.getItem('user.id')
      user.value.name = localStorage.getItem('user.name')
      user.value.email = localStorage.getItem('user.email')
      user.value.access = localStorage.getItem('user.access')
      user.value.refresh = localStorage.getItem('user.refresh')
    }
  }

  const setToken = (data: TokenData): void => {
    user.value.access = data.access
    user.value.refresh = data.refresh
    user.value.isAuthenticated = true

    localStorage.setItem('user.access', data.access)
    localStorage.setItem('user.refresh', data.refresh)
  }

  const removeToken = (): void => {
    user.value.refresh = null
    user.value.access = null
    user.value.isAuthenticated = false
    user.value.id = null
    user.value.name = null
    user.value.email = null

    localStorage.setItem('user.access', '')
    localStorage.setItem('user.refresh', '')
    localStorage.setItem('user.id', '')
    localStorage.setItem('user.name', '')
    localStorage.setItem('user.email', '')
  }

  const setUserInfo = (userData: User): void => {
    user.value.id = userData.id
    user.value.name = userData.name
    user.value.email = userData.email

    if (user.value.id && user.value.name && user.value.email) {
      localStorage.setItem('user.id', user.value.id)
      localStorage.setItem('user.name', user.value.name)
      localStorage.setItem('user.email', user.value.email)
    }
  }

  const refreshToken = async (): Promise<void> => {
    try {
      const response = await axios.post('/api/refresh/', {
        refresh: user.value.refresh
      })
      user.value.access = response.data.access
      localStorage.setItem('user.access', response.data.access)
      axios.defaults.headers.common['Authorization'] =
        `Bearer ${response.data.access}`
    } catch {
      removeToken()
    }
  }

  const logout = (): void => {
    removeToken()
    window.location.href = '/'
  }

  const signup = (formData: SignupFormData): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post('/api/signup/', formData)
        .then(() => resolve())
        .catch(error => reject(error))
    })
  }

  return {
    user,
    initializeStore,
    removeToken,
    setToken,
    setUserInfo,
    refreshToken,
    logout,
    signup
  }
})
