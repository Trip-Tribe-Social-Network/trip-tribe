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
          console.error('Error fetching posts:', error)
          reject(error)
        })
    })
  }

  const createPost = (body: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post('/api/posts/create/', body)
        .then(async () => {
          await fetchPosts()
          resolve()
        })
        .catch(error => {
          console.error('Error creating post:', error)
          reject(error)
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
          console.error('Error fetching trends:', error)
          reject(error)
        })
    })
  }

  const getTrendPosts = (trendId: string): Promise<Post[]> => {
    return new Promise((resolve, reject) => {
      axios
        .get(`/api/posts/?trend=${trendId}/`)
        .then(response => {
          posts.value = response.data
          resolve(response.data)
        })
        .catch(error => reject(error))
    })
  }

  const likePost = (postId: string): Promise<void> => {
    return new Promise((resolve, reject) => {
      axios
        .post(`/api/posts/${postId}/like/`)
        .then(response => {
          posts.value = response.data
          resolve(response.data)
        })
        .catch(error => reject(error))
    })
  }

  return {
    posts,
    fetchPosts,
    createPost,
    getTrends,
    getTrendPosts,
    trends,
    likePost
  }
})
