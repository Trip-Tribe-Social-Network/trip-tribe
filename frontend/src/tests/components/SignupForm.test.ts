import { beforeEach, describe, expect, test, vi } from 'vitest'
import { fireEvent, render, waitFor } from '@testing-library/vue'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createVuetify } from 'vuetify'
import SignupForm from '@/components/signup/SignupForm.vue'
import { createPinia } from 'pinia'
import axios from 'axios'

const vuetify = createVuetify({ components, directives })

describe('SignupForm', () => {
  let wrapper: any

  const createSignupFormComponent = () => {
    const pinia = createPinia()
    pinia.state.value = { ...pinia.state.value }

    return render(SignupForm, {
      global: {
        plugins: [vuetify, pinia]
      }
    })
  }

  const fillFormAndSubmit = async () => {
    await fireEvent.update(wrapper.getByLabelText('Username'), 'username')
    await fireEvent.update(wrapper.getByLabelText('Email'), 'test@test.com')
    await fireEvent.update(wrapper.getByLabelText('Password'), 'Password1!')
    await fireEvent.update(
      wrapper.getByLabelText('Confirm password'),
      'Password1!'
    )
    await fireEvent.click(wrapper.getByText('Sign Up'))
  }

  beforeEach(() => {
    wrapper = createSignupFormComponent()
  })

  describe('username field', () => {
    test('should display error message if field is empty', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Username'), '')
      await findByText('Username is required')
    })
    test('should display error message if username is invalid', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Username'), 'aa')
      await findByText('Username must be at least 3 characters')
    })
  })
  describe('email field', () => {
    test('should display error message if field is empty', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Email'), '')
      await findByText('Email is required')
    })
    test('should display error message if email is invalid', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Email'), 'invalid-email')
      await findByText('Email must be valid')
    })
  })
  describe('password field', () => {
    test('should display error message if field is empty', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Password'), '')
      await findByText('Password is required')
    })
    test('should display error message if password is less than 8 characters', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'pass')
      await findByText('Password must be at least 8 characters')
    })
    test('should display error message if password is not containing uppercase letters', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'password')
      await findByText('Password must contain uppercase letters')
    })
    test('should display error message if password is not containing special character', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'Password')
      await findByText('Password must have at least one special character')
    })
    test('should display error message if password is not matching confirm password', async () => {
      const { findByText, getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Password'), 'Password1!')
      await fireEvent.update(getByLabelText('Confirm password'), 'Password2!')
      await findByText('Passwords do not match')
    })
  })
  describe('reset button', () => {
    test('should reset all fields when clicked', async () => {
      const { getByLabelText } = createSignupFormComponent()
      await fireEvent.update(getByLabelText('Username'), 'username')
      await fireEvent.update(getByLabelText('Email'), '')
    })
  })
  describe('submit form', () => {
    test('should call emit sucessful message when form is submitted with expected data', async () => {
      axios.post = vi.fn().mockResolvedValue({})
      await fillFormAndSubmit()
      await waitFor(() => {
        expect(wrapper.emitted()['show-snackbar'][0]).toEqual([
          {
            message: 'Signup successful!',
            type: 'success'
          }
        ])
      })
    })
    test('should call emit error message when form is submitted with unexpected data', async () => {
      axios.post = vi.fn().mockRejectedValue(new Error('error'))
      await fillFormAndSubmit()
      await waitFor(() => {
        expect(wrapper.emitted()['show-snackbar'][0]).toEqual([
          {
            message: 'Failed to signup',
            type: 'error'
          }
        ])
      })
    })
  })
})
