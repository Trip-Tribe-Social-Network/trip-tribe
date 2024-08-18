import router from '@/router/index'

export const navigate = (path: string) => router.push(path)
export const userUUID = () => localStorage.getItem('user.id')
