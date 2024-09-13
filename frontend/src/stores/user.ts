import { ref } from 'vue'
import axios from 'axios'
import { defineStore } from 'pinia'
import type {
  User,
  TokenData,
  SignupFormData,
  LoginFormData,
  Notification
} from '@/models/user'

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({
    isAuthenticated: false,
    friends: [],
    friends_count: 0,
    id: null,
    name: null,
    bio: null,
    email: null,
    access: null,
    refresh: null
  })

  const notifications = ref<Notification[]>([])

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
    user.value.refresh = ''
    user.value.access = ''
    user.value.isAuthenticated = false
    user.value.id = ''
    user.value.name = ''
    user.value.email = ''

    localStorage.removeItem('user.access')
    localStorage.removeItem('user.refresh')
    localStorage.removeItem('user.id')
    localStorage.removeItem('user.name')
    localStorage.removeItem('user.email')
  }

  const setUserInfo = (userData: User): void => {
    user.value.id = userData.id
    user.value.avatar = userData.avatar
    user.value.friends = userData.friends
    user.value.friends_count = userData.friends_count
    user.value.name = userData.name
    user.value.bio = userData.bio
    user.value.email = userData.email

    if (user.value.id && user.value.name && user.value.email) {
      localStorage.setItem('user.id', user.value.id)
      localStorage.setItem('user.name', user.value.name)
      localStorage.setItem('user.email', user.value.email)
    }
  }

  const getBaseUser = (): Promise<User> => {
    return new Promise((resolve, reject) => {
      if (user.value.access) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${user.value.access}`
      }

      axios
        .get('/api/me/')
        .then(response => {
          resolve(response.data)
          setUserInfo(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const refreshToken = async (): Promise<void> => {
    try {
      const response = await axios.post('/api/refresh/', {
        refresh: user.value.refresh
      })
      user.value.access = response.data.access
      localStorage.setItem('user.access', response.data.access)
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    } catch {
      removeToken()
    }
  }

  const logout = (): void => {
    removeToken()
    user.value.id = null
    user.value.name = null
    user.value.email = null
    user.value.avatar = null
    user.value.access = null
    user.value.refresh = null
    user.value.isAuthenticated = false
    window.location.href = '/'
  }

  const signup = (formData: SignupFormData): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post('/api/signup/', formData)
        .then(() => resolve())
        .catch(error => reject(new Error(error)))
    })
  }

  const login = (loginFormData: LoginFormData): Promise<TokenData> => {
    return new Promise((resolve, reject) => {
      axios
        .post('/api/login/', loginFormData)
        .then(response => {
          setToken(response.data)
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const getNotifications = (): Promise<Notification[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get('/api/notifications/')
        .then(response => {
          notifications.value = response.data
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  return {
    user,
    initializeStore,
    removeToken,
    setToken,
    setUserInfo,
    refreshToken,
    getBaseUser,
    getNotifications,
    notifications,
    logout,
    login,
    signup
  }
})
