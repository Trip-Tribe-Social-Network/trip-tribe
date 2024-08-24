import { describe, beforeEach, test, expect, vi } from 'vitest'
import { useChatStore } from '@/stores/chat'
import { CONVERSATIONS, CONVERSATION } from '@/tests/mocks/chat'
import { createPinia, setActivePinia } from 'pinia'
import axios from 'axios'

describe('chat store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test('get conversations', async () => {
    const store = useChatStore()

    axios.get = vi.fn().mockResolvedValue({ data: CONVERSATIONS })
    const spy = vi.spyOn(axios, 'get')
    await store.getConversations()
    expect(spy).toHaveBeenCalledWith(`/api/chat/`)
  })

  test('get messages', async () => {
    const store = useChatStore()

    const ACTIVE_CONVERSATION_ID = 'ce77b652-84fb-47f5-9210-05669162d8e1'
    store.activeConversationId = ACTIVE_CONVERSATION_ID

    axios.get = vi.fn().mockResolvedValue({ data: CONVERSATION })
    const spy = vi.spyOn(axios, 'get')
    await store.getMessages(ACTIVE_CONVERSATION_ID)
    expect(spy).toHaveBeenCalledWith(`/api/chat/${ACTIVE_CONVERSATION_ID}/`)
  })
  test('send direct message', async () => {
    const store = useChatStore()

    const USER_UUID = 'ce77b652-84fb-47f5-9210-05669162d8e1'

    axios.get = vi.fn().mockResolvedValue({ data: { id: USER_UUID } })
    const spy = vi.spyOn(axios, 'get')
    await store.sendDirectMessage(USER_UUID)
    expect(spy).toHaveBeenCalledWith(`/api/chat/${USER_UUID}/get-or-create/`)
  })
  test('send message', async () => {
    const store = useChatStore()

    const MESSAGE = 'Hello, world!'
    store.activeConversationId = 'ce77b652-84fb-47f5-9210-05669162d8e1'

    axios.post = vi.fn().mockResolvedValue({ data: { body: MESSAGE } })
    const spy = vi.spyOn(axios, 'post')
    await store.sendMessage(MESSAGE)
    expect(spy).toHaveBeenCalledWith(`/api/chat/${store.activeConversationId}/send/`, {
      body: MESSAGE
    })
  })
})
