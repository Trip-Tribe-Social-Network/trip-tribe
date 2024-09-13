export const SIGNUP_FORM_DATA = {
  name: 'test',
  email: 'test@test.com',
  password1: 'Test1234!',
  password2: 'Test1234!'
}

export const LOGIN_FORM_DATA = {
  email: 'test@test.com',
  password: 'Test1234!'
}

export const TOKEN_DATA = {
  access: 'fake-access-token',
  refresh: 'fake-refresh-token'
}

export const USER_STATE = {
  isAuthenticated: false,
  id: null,
  name: null,
  email: null,
  access: null,
  refresh: null
}

export const NOTIFICATIONS = [
  {
    id: '1',
    body: 'test notification',
    type_of_notification: 'test',
    post_id: '1',
    created_for_id: '1'
  },
  {
    id: '2',
    body: 'test notification 2',
    type_of_notification: 'test',
    post_id: '2',
    created_for_id: '2'
  }
]
