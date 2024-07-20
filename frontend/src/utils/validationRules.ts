export const usernameRules = [
  (v: string) => !!v || 'Username is required',
  (v: string) => v.length >= 3 || 'Username must be at least 3 characters'
]

export const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid'
]

export const passwordRules = [
  (v: string) => !!v || 'Password is required',
  (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
  (v: string) => /[A-Z]/.test(v) || 'Password must contain uppercase letters',
  (v: string) =>
    /\W|_/.test(v) || 'Password must have at least one special character'
]

export const confirmPasswordRules = (password: string) => [
  (v: string) => v === password || 'Passwords do not match'
]

export const clientnameRules = [(v: string) => !!v || 'Client name is required']

export const adressRules = [(v: string) => !!v || 'Address is required']

export const imageRules = [(v: File) => !!v || 'Image is required']
