export interface UserFriends {
  user: User
  friends: User[]
  requests: Request[]
}

export interface Request {
  id: string
  created_by: User
  created_at: string
  status: string
}

export interface User {
  id: string
  name: string
  email: string
  friends: User[]
  get_avatar: string
  friends_count: number
}
