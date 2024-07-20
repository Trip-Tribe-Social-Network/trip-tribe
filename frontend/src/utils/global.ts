import router from '@/router/index'

export const resetForm = (): void => window.location.reload()

export const getImageUrl = (image: any) => {
  if (image instanceof File) {
    return URL.createObjectURL(image)
  }
  return image
}

export const navigate = (path: string) => router.push(path)
