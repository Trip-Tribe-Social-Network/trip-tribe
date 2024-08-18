export interface Profile {
  posts: any[]
  user: UserProfile
}

export interface UserProfile {
  id: string
  name: string
  email: string
  get_avatar: string | undefined
  friends_count: number
}
export interface Post {
  id: string
  body: string
  created_at_formatted: string
  created_by: Profile
}
