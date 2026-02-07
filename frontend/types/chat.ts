/**
 * Chat type definitions
 */

export type ChatRole = 'user' | 'assistant'

export interface ChatMessage {
  id: string
  role: ChatRole
  content: string
}

export interface ChatRequest {
  conversation_id?: number | null
  message: string
}

export interface ChatResponse {
  conversation_id: number
  response: string
  tool_calls: string[]
}
