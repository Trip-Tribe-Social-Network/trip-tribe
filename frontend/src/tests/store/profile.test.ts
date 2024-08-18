import { describe, beforeEach, test, expect, vi } from 'vitest'
import { useProfileStore } from '@/stores/profile'
import { CURRENT_USER_PROFILE, EDIT_PROFILE_FORM } from '@/tests/mocks/profile'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

describe('profile store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test('get profile feed success', async () => {
    const store = useProfileStore()

    axios.get = vi.fn().mockResolvedValue({ data: CURRENT_USER_PROFILE })
    const spy = vi.spyOn(axios, 'get')
    await store.getFeed(CURRENT_USER_PROFILE.user.id)
    expect(spy).toHaveBeenCalledWith(
      `/api/posts/profile/${CURRENT_USER_PROFILE.user.id}/`
    )
  })
  test('edit user profile success', async () => {
    const store = useProfileStore()

    const formData = new FormData()
    formData.append('name', EDIT_PROFILE_FORM.name)
    formData.append('email', EDIT_PROFILE_FORM.email)
    formData.append('avatar', EDIT_PROFILE_FORM.avatar)

    axios.post = vi.fn().mockResolvedValue({})
    const spy = vi.spyOn(axios, 'post')
    await store.editUserProfile(formData)
    expect(spy).toHaveBeenCalledWith('/api/edit_profile/', formData)
  })
})
