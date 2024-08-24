import { describe, expect, test } from 'vitest'
import { render, screen } from '@testing-library/vue'
import ChatCard from '@/components/chat/ChatCard.vue'
import { CONVERSATION } from '@/tests/mocks/chat'
import { createVuetify } from 'vuetify'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router/index'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({ components, directives })

global.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}

describe('ChatCard', () => {
  const createChatCard = () => {
    return render(ChatCard, {
      props: {
        messages: CONVERSATION.messages
      },
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            stubActions: false
          }),
          router
        ],
        stubs: {
          transition: false
        }
      }
    })
  }

  test('renders messages', async () => {
    createChatCard()
    const messages = await screen.findAllByTestId('message')
    expect(messages).toHaveLength(CONVERSATION.messages.length)
  })
})
