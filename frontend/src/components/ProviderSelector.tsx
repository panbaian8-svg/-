import { useState, useEffect } from 'react'
import { getProvider, switchProvider } from '../api/client'

interface ProviderSelectorProps {
  onProviderChange?: (provider: string) => void
}

export default function ProviderSelector({ onProviderChange }: ProviderSelectorProps) {
  const [provider, setProvider] = useState<string>('deepseek')
  const [availableProviders, setAvailableProviders] = useState<string[]>(['deepseek', 'minimax'])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProvider()
  }, [])

  const fetchProvider = async () => {
    try {
      const response = await getProvider()
      setProvider(response.data.provider)
      setAvailableProviders(response.data.available_providers)
    } catch (err) {
      console.error('Failed to fetch provider:', err)
    }
  }

  const handleSwitch = async (newProvider: string) => {
    if (newProvider === provider) return

    setLoading(true)
    setError(null)
    try {
      const response = await switchProvider(newProvider)
      setProvider(response.data.provider)
      onProviderChange?.(response.data.provider)
    } catch (err: any) {
      setError(err.response?.data?.detail || '切换失败')
    } finally {
      setLoading(false)
    }
  }

  const providerLabels: Record<string, string> = {
    deepseek: 'DeepSeek',
    minimax: 'MiniMax'
  }

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-gray-500">AI 提供商:</span>
      <div className="flex space-x-1">
        {availableProviders.map((p) => (
          <button
            key={p}
            onClick={() => handleSwitch(p)}
            disabled={loading}
            className={`px-3 py-1 text-sm rounded-md transition-colors ${
              provider === p
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {providerLabels[p] || p}
          </button>
        ))}
      </div>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  )
}
