export interface User {
  isAuthenticated: boolean
  id: string | null
  name: string | null
  email: string | null
  access: string | null
  refresh: string | null
}

export interface SignupFormData {
  name: string | undefined
  email: string | undefined
  password1: string | undefined
  password2: string | undefined
}

export type TokenData = {
  access: string
  refresh: string
}
