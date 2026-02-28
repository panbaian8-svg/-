import { useState } from 'react'
import api from '../api/client'

interface QAInterfaceProps {
  documentId: string
}

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function QAInterface({ documentId }: QAInterfaceProps) {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAsk = async () => {
    if (!question.trim()) return

    const userMessage: Message = { role: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    setQuestion('')
    setLoading(true)
    setError(null)

    try {
      const response = await api.post('/qa/ask', {
        question,
        document_id: documentId,
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.answer,
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err: any) {
      setError(err.response?.data?.detail || '提问失败')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleAsk()
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold mb-4">智能问答</h2>

        {/* Chat Messages */}
        <div className="h-[400px] overflow-y-auto mb-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 py-8">
              开始提问吧，我会根据文档内容回答你的问题
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-blue-50 ml-auto max-w-[80%]'
                  : 'bg-gray-50 mr-auto max-w-[80%]'
              }`}
            >
              {msg.content}
            </div>
          ))}
          {loading && (
            <div className="text-gray-400">思考中...</div>
          )}
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
            {error}
          </div>
        )}

        {/* Input */}
        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="输入你的问题..."
            className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handleAsk}
            disabled={!question.trim() || loading}
            className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            提问
          </button>
        </div>
      </div>
    </div>
  )
}
