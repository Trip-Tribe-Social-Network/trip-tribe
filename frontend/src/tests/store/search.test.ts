import { describe, beforeEach, test, expect, vi } from 'vitest'
import { useSearchStore } from '@/stores/search'
import { USER_FOUND } from '@/tests/mocks/search'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

describe('search store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test('search query success', async () => {
    const store = useSearchStore()

    axios.post = vi.fn().mockResolvedValue(USER_FOUND)
    const spy = vi.spyOn(axios, 'post')
    await store.search('claire')
    expect(spy).toHaveBeenCalledWith(`/api/search/`, { query: 'claire' })
  })
})
