import type { User } from '@/models/friends'

export interface User {
  isAuthenticated?: boolean
  id: string | null
  name: string | null
  email: string | null
  bio?: string | null
  access?: string | null
  refresh?: string | null
  friends: User[]
  friends_count: number
  avatar?: string | null | undefined
}

export interface SignupFormData {
  name: string | undefined
  email: string | undefined
  password1: string | undefined
  password2: string | undefined
}

export interface LoginFormData {
  email: string | undefined
  password: string | undefined
}

export type TokenData = {
  id: string
  access: string
  refresh: string
}
