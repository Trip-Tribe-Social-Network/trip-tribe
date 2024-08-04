import { createRouter, createWebHistory } from 'vue-router'
import Signup from '@/views/SignupView.vue'
import Login from '@/views/LoginView.vue'
import Chat from '@/views/ChatView.vue'
import Feed from '@/views/FeedView.vue'
import Friends from '@/views/FriendsView.vue'
import Profile from '@/views/ProfileView.vue'
import Messages from '@/views/MessagesView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Login
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: Signup
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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export { routes }

export default router
