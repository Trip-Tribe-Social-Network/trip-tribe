import { describe, beforeEach, test, expect, vi } from 'vitest'
import { useUserStore } from '@/stores/user'
import { SIGNUP_FORM_DATA } from '@/tests/mocks/user'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

describe('app release and eula store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  describe('user store', () => {
    test('user signup success', async () => {
      const store = useUserStore()

      axios.post = vi.fn().mockResolvedValue({})
      const spy = vi.spyOn(axios, 'post')
      await store.signup(SIGNUP_FORM_DATA)
      expect(spy).toHaveBeenCalledWith('/api/signup/', SIGNUP_FORM_DATA)
    })
  })
})
