import { describe, expect, test } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import ConversationsTab from '@/components/chat/ConversationsTab.vue'
import { CONVERSATIONS } from '@/tests/mocks/chat'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router/index'

const vuetify = createVuetify({ components, directives })

describe('ConversationsTab', () => {
  const createConversationsTab = () => {
    return render(ConversationsTab, {
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            initialState: {
              chat: {
                conversations: CONVERSATIONS
              }
            },
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

  test('should display friends name', async () => {
    const { getAllByTestId } = createConversationsTab()
    await waitFor(() => {
      expect(getAllByTestId('user-name').length).toBe(4)
    })
  })

  test('should display friends avatar', async () => {
    const { getAllByTestId } = createConversationsTab()
    await waitFor(() => {
      expect(getAllByTestId('user-avatar').length).toBe(4)
    })
  })

  test('should redirect to conversation on button click', async () => {
    const { getAllByText } = createConversationsTab()

    const buttons = getAllByText('Go')
    const firstConversationButton = buttons[0]
    await fireEvent.click(firstConversationButton)

    await waitFor(() => {
      expect(router.push(`/conversation/${CONVERSATIONS[0].id}`)).toBeTruthy()
    })
  })
})
