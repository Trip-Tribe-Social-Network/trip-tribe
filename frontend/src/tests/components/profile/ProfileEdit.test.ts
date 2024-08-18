import { beforeAll, beforeEach, describe, expect, test, vi } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import ProfileEdit from '@/components/profile/ProfileEdit.vue'
import { CURRENT_USER_PROFILE } from '@/tests/mocks/profile'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import { createPinia, setActivePinia } from 'pinia'
import { createTestingPinia } from '@pinia/testing'
import axios from 'axios'

const vuetify = createVuetify({ components, directives })

describe('ProfileEdit', () => {
  const createProfileEditComponent = () => {
    return render(ProfileEdit, {
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            initialState: {
              profile: {
                user: CURRENT_USER_PROFILE.user
              }
            },
            stubActions: false
          })
        ]
      }
    })
  }

  beforeAll(() => {
    localStorage.setItem('user.id', CURRENT_USER_PROFILE.user.id)
  })

  beforeEach(() => {
    setActivePinia(createPinia())
  })

  test('should close the dialog when the close button is clicked', async () => {
    const { getByTestId, emitted } = createProfileEditComponent()

    await fireEvent.click(getByTestId('edit-profile'))
    await fireEvent.click(getByTestId('close-dialog'))
    await waitFor(() => {
      expect(emitted()['close-dialog']).toBeTruthy()
    })
  })

  test('should edit profile and saves changes', async () => {
    axios.post = vi.fn().mockResolvedValue({ message: 'Profile successfully updated' })
    axios.get = vi.fn().mockResolvedValue({ data: CURRENT_USER_PROFILE })
    const { getByTestId, getByLabelText, emitted } = createProfileEditComponent()

    await fireEvent.click(getByTestId('edit-profile'))
    await fireEvent.update(getByLabelText('Name'), 'John Doe')
    await fireEvent.update(getByLabelText('Email'), 'john.doe@gmail.com')
    await fireEvent.update(getByLabelText('Avatar'), 'john.png')
    await fireEvent.click(getByTestId('save-changes'))

    const expectedFormData = new FormData()
    expectedFormData.append('name', 'John Doe')
    expectedFormData.append('email', 'john.doe@gmail.com')
    expectedFormData.append('avatar', 'john.png')

    await waitFor(() => {
      expect(emitted()['show-snackbar'][0]).toEqual([
        {
          message: 'Profile successfully updated',
          type: 'success'
        }
      ])
    })
  })
})
