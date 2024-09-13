import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'
import type { Post, Trend } from '@/models/post'

export const usePostStore = defineStore('post', () => {
  const posts = ref<Post[]>([])
  const trends = ref<Trend[]>([])

  const fetchPosts = (): Promise<Post[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get('/api/posts/')
        .then(response => {
          posts.value = response.data
          resolve(posts.value)
        })
        .catch(error => {
          reject(new Error(error))
        })
    })
  }

  const createPost = (formData: FormData): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post('/api/posts/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(async () => {
          await fetchPosts()
          resolve()
        })
        .catch(error => {
          reject(new Error(error))
        })
    })
  }

  const getTrends = (): Promise<Trend[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get('/api/posts/trends/')
        .then(response => {
          trends.value = response.data
          resolve(trends.value)
        })
        .catch(error => {
          reject(new Error(error))
        })
    })
  }

  const getTrendPosts = (trendId: string): Promise<Post[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/posts/?trend=${trendId}`)
        .then(response => {
          posts.value = response.data
          resolve(response.data)
        })
        .catch(error => {
          reject(new Error(error))
        })
    })
  }

  const likePost = (postId: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/posts/${postId}/like/`)
        .then(response => {
          fetchPosts()
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  const deletePost = (postId: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/posts/${postId}/delete/`)
        .then(response => {
          fetchPosts()
          resolve(response.data)
        })
        .catch(error => reject(new Error(error)))
    })
  }

  return {
    posts,
    fetchPosts,
    createPost,
    getTrends,
    getTrendPosts,
    trends,
    likePost,
    deletePost
  }
})
