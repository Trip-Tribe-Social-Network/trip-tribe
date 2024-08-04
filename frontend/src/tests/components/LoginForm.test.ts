import { USER_STATE, TOKEN_DATA } from '@/tests/mocks/user'
import { describe, expect, test, vi, beforeEach } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import LoginForm from '@/components/login/LoginForm.vue'
import { createTestingPinia } from '@pinia/testing'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from '@/router/index'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

const vuetify = createVuetify({ components, directives })

describe('LoginForm', () => {
  let wrapper: any
  const createLoginFormComponent = (
    initialState = { user: { user: USER_STATE } }
  ) => {
    return render(LoginForm, {
      global: {
        plugins: [
          vuetify,
          createTestingPinia({
            initialState,
            stubActions: false
          }),
          router
        ]
      }
    })
  }

  const fillFormAndSubmit = async () => {
    await fireEvent.update(wrapper.getByLabelText('Email'), 'test@test.com')
    await fireEvent.update(wrapper.getByLabelText('Password'), 'Password1!')
    await fireEvent.click(wrapper.getByTestId('login-button'))
  }

  beforeEach(() => {
    wrapper = createLoginFormComponent()
  })

  describe('email field', () => {
    test('should display error message if field is empty', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Email'), '')
      await findByText('Email is required')
    })

    test('should display error message if email is invalid', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Email'), 'invalid-email')
      await findByText('Email must be valid')
    })
  })

  describe('password field', () => {
    test('should display error message if field is empty', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Password'), '')
      await findByText('Password is required')
    })

    test('should display error message if password is less than 8 characters', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'pass')
      await findByText('Password must be at least 8 characters')
    })

    test('should display error message if password is not containing uppercase letters', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'password')
      await findByText('Password must contain uppercase letters')
    })

    test('should display error message if password is not containing special character', async () => {
      const { findByText, getByLabelText } = createLoginFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'Password')
      await findByText('Password must have at least one special character')
    })
  })

  describe('submit form', () => {
    test('should redirect to feed page when form is submitted with expected data', async () => {
      axios.post = vi.fn().mockResolvedValue(TOKEN_DATA)
      await fillFormAndSubmit()
      await waitFor(() => {
        expect(router.push('feed'))
      })
    })

    test('should call emit error message when form is submitted with unexpected data', async () => {
      axios.post = vi.fn().mockRejectedValue(new Error('error'))
      await fillFormAndSubmit()
      await waitFor(() => {
        expect(wrapper.emitted()['show-snackbar'][0]).toEqual([
          {
            message: 'Failed to login',
            type: 'error'
          }
        ])
      })
    })
  })
})
