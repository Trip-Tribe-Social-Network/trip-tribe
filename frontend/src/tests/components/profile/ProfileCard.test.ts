import { describe, expect, test, vi } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import ProfileCard from '@/components/profile/ProfileCard.vue'
import {
  CURRENT_USER_PROFILE,
  TARGET_USER_PROFILE,
  PROFILE_FRIENDS
} from '@/tests/mocks/profile'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { createTestingPinia } from '@pinia/testing'
import router from '@/router/index'
import type { Profile } from '@/models/profile'
import axios from 'axios'

const vuetify = createVuetify({ components, directives })

describe('ProfileCard', () => {
  const createProfileCardComponent = (profileData: Profile) => {
    return render(ProfileCard, {
      props: {
        user: profileData.user,
        posts: profileData.posts,
        friends: PROFILE_FRIENDS.friends
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

  test('should display the user name', () => {
    const { getByText } = createProfileCardComponent(CURRENT_USER_PROFILE)

    getByText('Olivia Smith')
  })

  test('should display the user avatar', () => {
    const { getByTestId } = createProfileCardComponent(CURRENT_USER_PROFILE)

    const avatar = getByTestId('avatar') as HTMLElement
    const avatarImg = avatar.querySelector('img')
    expect(avatarImg?.src).toBe(CURRENT_USER_PROFILE.user.get_avatar)
  })

  test('should display the accurate number of user friends', () => {
    const {} = createProfileCardComponent(CURRENT_USER_PROFILE)
    expect(CURRENT_USER_PROFILE.user.friends.length).toBe(6)
  })

  test('should display the accurate number of user posts', () => {
    createProfileCardComponent(CURRENT_USER_PROFILE)
    expect(CURRENT_USER_PROFILE.posts.length).toBe(2)
  })

  test('should send a friend request from one profile to another', async () => {
    axios.post = vi.fn().mockResolvedValue({ data: { message: 'Friend request sent' } })
    const { getByText, rerender, emitted } =
      createProfileCardComponent(CURRENT_USER_PROFILE)

    getByText('Olivia Smith')
    await rerender(TARGET_USER_PROFILE)
    getByText('Emily Johnson')
    getByText('Send request')
    await fireEvent.click(getByText('Send request'))
    await waitFor(() => {
      expect(emitted()['show-snackbar'][0]).toEqual([
        {
          message: 'Friend request sent',
          type: 'success'
        }
      ])
    })
  })
})
