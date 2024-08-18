import { describe, expect, test, vi } from 'vitest'
import { fireEvent, render } from '@testing-library/vue'
import FriendsCard from '@/components/friends/FriendsCard.vue'
import { CURRENT_USER_FRIENDS } from '@/tests/mocks/friends'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router/index'

const vuetify = createVuetify({ components, directives })

describe('FriendsCard', () => {
  const createFriendsCardComponent = () => {
    return render(FriendsCard, {
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            initialState: {
              friends: {
                friends: CURRENT_USER_FRIENDS.friends
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
    const { getByText } = createFriendsCardComponent()

    getByText('Olivia Smith')
  })
  test('should display friend avatar', () => {
    const { getByTestId } = createFriendsCardComponent()

    const avatar = getByTestId('avatar') as HTMLElement
    const avatarImg = avatar.querySelector('img')
    expect(avatarImg?.src).toBe(CURRENT_USER_FRIENDS.friends[0].get_avatar)
  })
  test('should redirect to the friend profile page when clicking on profile button', async () => {
    const { getByText } = createFriendsCardComponent()
    const push = vi.spyOn(router, 'push')
    await fireEvent.click(getByText('see profile'))
    expect(push).toHaveBeenCalledWith(`/profile/${CURRENT_USER_FRIENDS.friends[0].id}`)
  })
})
