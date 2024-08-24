import { UserProfile } from '@/models/profile'

export interface Conversation {
  id: string
  users: string[]
  modified_at_formatted: string
  messages: Message[]
}

export type Conversations = Conversation[]

export interface Message {
  id: string
  sent_to: UserProfile
  created_by: UserProfile
  created_at_formatted: string
  body: string
}
