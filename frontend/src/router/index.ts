import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Signup from '@/views/SignupView.vue'
import Login from '@/views/LoginView.vue'
import Chat from '@/views/ChatView.vue'
import Feed from '@/views/FeedView.vue'
import Friends from '@/views/FriendsView.vue'
import Profile from '@/views/ProfileView.vue'
import Messages from '@/views/MessagesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Signup
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/chat',
      name: 'chat',
      component: Messages
    },
    {
      path: '/conversation',
      name: 'conversation',
      component: Chat
    },
    {
      path: '/feed',
      name: 'feed',
      component: Feed
    },
    {
      path: '/friends',
      name: 'friends',
      component: Friends
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    }
  ]
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.matched.some((record) => record.meta.requireLogin) && !userStore.user.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
