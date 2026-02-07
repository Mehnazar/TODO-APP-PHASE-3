'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Bot, LogOut, Send, User } from 'lucide-react'
import { auth } from '@/lib/auth'
import { chatAPI } from '@/lib/api'
import { useToast } from '@/hooks/useToast'
import type { ChatMessage, ChatResponse } from '@/types/chat'

const CONVERSATION_KEY = 'chat_conversation_id'

export default function ChatPage() {
  const router = useRouter()
  const toast = useToast()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const [conversationId, setConversationId] = useState<number | null>(null)
  const [userName, setUserName] = useState<string>('User')
  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (!auth.isAuthenticated()) {
      router.push('/login')
      return
    }

    const user = auth.getUser()
    if (user?.name) {
      setUserName(user.name)
    }

    const storedId = window.localStorage.getItem(CONVERSATION_KEY)
    if (storedId) {
      const parsed = Number(storedId)
      if (!Number.isNaN(parsed)) {
        setConversationId(parsed)
      }
    }
  }, [router])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, sending])

  const resetConversation = () => {
    setConversationId(null)
    setMessages([])
    window.localStorage.removeItem(CONVERSATION_KEY)
  }

  const handleSend = async () => {
    const user = auth.getUser()
    if (!user || !input.trim()) return

    const messageText = input.trim()
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: messageText,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setSending(true)

    const sendRequest = async (overrideConversationId?: number | null) => {
      return await chatAPI.sendMessage(user.id, {
        conversation_id: overrideConversationId ?? conversationId ?? undefined,
        message: messageText,
      })
    }

    try {
      let response: ChatResponse
      try {
        response = await sendRequest()
      } catch (err: any) {
        const errorCode = err.response?.data?.detail?.error?.code
        if (errorCode === 'CONVERSATION_NOT_FOUND') {
          resetConversation()
          response = await sendRequest(null)
        } else {
          throw err
        }
      }

      if (response.conversation_id && response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id)
        window.localStorage.setItem(CONVERSATION_KEY, String(response.conversation_id))
      }

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.response,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err: any) {
      const message = err.response?.data?.detail?.error?.message || 'Failed to send message'
      toast.error(message)
    } finally {
      setSending(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!sending) {
        handleSend()
      }
    }
  }

  const handleLogout = () => {
    auth.logout()
    router.push('/login')
  }

  const handleNewChat = () => {
    resetConversation()
  }

  const emptyState = useMemo(() => messages.length === 0, [messages.length])

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-slate-950 to-slate-900 text-white flex flex-col">
      <header className="border-b border-slate-800/60 bg-slate-900/80 backdrop-blur">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-600/20 flex items-center justify-center">
              <Bot className="w-5 h-5 text-purple-300" />
            </div>
            <div>
              <p className="text-sm text-purple-200">ChatKit</p>
              <h1 className="text-xl font-semibold">Todo Assistant</h1>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-slate-800/60 rounded-lg border border-slate-700">
              <User className="w-4 h-4 text-purple-300" />
              <span className="text-sm font-medium">{userName}</span>
            </div>
            <button
              onClick={handleNewChat}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border border-slate-700 bg-slate-800/60 hover:bg-slate-800 transition-colors"
            >
              <span className="text-sm">New chat</span>
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border border-slate-700 bg-slate-800/60 hover:bg-slate-800 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span className="text-sm hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 md:p-6 min-h-[60vh] flex flex-col">
            {emptyState ? (
              <div className="flex-1 flex items-center justify-center text-center">
                <div className="max-w-md">
                  <div className="text-5xl mb-4">💬</div>
                  <h2 className="text-xl font-semibold mb-2">Start a conversation</h2>
                  <p className="text-slate-300">
                    Ask me to add, list, update, complete, or delete tasks.
                  </p>
                </div>
              </div>
            ) : (
              <div className="flex-1 space-y-4 overflow-y-auto pr-2">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm md:text-base leading-relaxed ${
                        message.role === 'user'
                          ? 'bg-purple-600 text-white'
                          : 'bg-slate-800 text-slate-100 border border-slate-700'
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                ))}
                {sending && (
                  <div className="flex justify-start">
                    <div className="max-w-[80%] rounded-2xl px-4 py-3 text-sm md:text-base bg-slate-800 text-slate-300 border border-slate-700">
                      Thinking...
                    </div>
                  </div>
                )}
                <div ref={endRef} />
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-800/60 bg-slate-900/80 backdrop-blur">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex flex-col sm:flex-row gap-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Message the assistant..."
              className="flex-1 resize-none rounded-xl bg-slate-800/70 border border-slate-700 px-4 py-3 text-sm md:text-base focus:outline-none focus:border-purple-500 min-h-[52px]"
              disabled={sending}
              rows={1}
            />
            <button
              onClick={handleSend}
              disabled={sending || !input.trim()}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-purple-600 hover:bg-purple-700 disabled:bg-purple-900 disabled:cursor-not-allowed px-5 py-3 text-sm md:text-base font-semibold transition-colors"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </div>
        </div>
      </footer>
    </div>
  )
}
