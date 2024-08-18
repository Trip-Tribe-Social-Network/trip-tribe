import { describe, expect, test, vi } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import FriendsRequest from '@/components/friends/FriendsRequest.vue'
import { CURRENT_USER_FRIENDS } from '@/tests/mocks/friends'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router/index'
import axios from 'axios'

const vuetify = createVuetify({ components, directives })

describe('FriendsRequest', () => {
  const createFriendsRequestComponent = () => {
    return render(FriendsRequest, {
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            initialState: {
              friends: {
                requests: CURRENT_USER_FRIENDS.requests
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

  test('should display friend name', () => {
    const { getByText } = createFriendsRequestComponent()

    getByText('Diego Fernandez')
  })
  test('should display friend avatar', () => {
    const { getByTestId } = createFriendsRequestComponent()

    const avatar = getByTestId('avatar') as HTMLElement
    const avatarImg = avatar.querySelector('img')
    expect(avatarImg?.src).toBe(CURRENT_USER_FRIENDS.requests[0].created_by.get_avatar)
  })
  test('should accept request on click', async () => {
    axios.post = vi
      .fn()
      .mockResolvedValue({ data: { message: 'Friend request updated successfully' } })
    const { getByText, emitted } = createFriendsRequestComponent()

    await fireEvent.click(getByText('Accept'))
    await waitFor(() => {
      expect(emitted()['show-snackbar'][0]).toEqual([
        {
          message: 'Friend request updated successfully',
          type: 'success'
        }
      ])
    })
  })
  test('should decline request on click', async () => {
    axios.post = vi
      .fn()
      .mockResolvedValue({ data: { message: 'Friend request updated successfully' } })
    const { getByText, emitted } = createFriendsRequestComponent()

    await fireEvent.click(getByText('Decline'))
    await waitFor(() => {
      expect(emitted()['show-snackbar'][0]).toEqual([
        {
          message: 'Friend request updated successfully',
          type: 'success'
        }
      ])
    })
  })
  test('should fail to update friend request on click', async () => {
    axios.post = vi.fn().mockRejectedValue(new Error('Failed to update friend request'))
    const { getByText, emitted } = createFriendsRequestComponent()

    await fireEvent.click(getByText('Decline'))
    await waitFor(() => {
      expect(emitted()['show-snackbar'][0]).toEqual([
        {
          message: 'Failed to update friend request',
          type: 'error'
        }
      ])
    })
  })
})
