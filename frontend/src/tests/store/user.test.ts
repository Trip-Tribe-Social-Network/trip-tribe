import { describe, beforeEach, test, expect, vi } from 'vitest'
import { useUserStore } from '@/stores/user'
import {
  SIGNUP_FORM_DATA,
  LOGIN_FORM_DATA,
  TOKEN_DATA
} from '@/tests/mocks/user'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

describe('user store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test('user signup success', async () => {
    const store = useUserStore()

    axios.post = vi.fn().mockResolvedValue({})
    const spy = vi.spyOn(axios, 'post')
    await store.signup(SIGNUP_FORM_DATA)
    expect(spy).toHaveBeenCalledWith('/api/signup/', SIGNUP_FORM_DATA)
  })
  test('user login success', async () => {
    const store = useUserStore()

    axios.post = vi.fn().mockResolvedValue({
      data: TOKEN_DATA
    })

    const spy = vi.spyOn(axios, 'post')
    await store.login(LOGIN_FORM_DATA)
    expect(spy).toHaveBeenCalledWith('/api/login/', LOGIN_FORM_DATA)
  })
})
