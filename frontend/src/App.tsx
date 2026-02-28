import { useState } from 'react'
import UploadFile from './components/UploadFile'
import KnowledgeMap from './components/KnowledgeMap'
import QAInterface from './components/QAInterface'
import ProviderSelector from './components/ProviderSelector'

function App() {
  const [currentDocument, setCurrentDocument] = useState<string | null>(null)
  const [currentView, setCurrentView] = useState<'upload' | 'map' | 'qa'>('upload')

  const handleDocumentUploaded = (documentId: string) => {
    setCurrentDocument(documentId)
    setCurrentView('map')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">StudyFlow AI - 智能助学系统</h1>
          <ProviderSelector />
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex space-x-8">
            <button
              onClick={() => setCurrentView('upload')}
              className={`py-4 px-2 border-b-2 ${
                currentView === 'upload'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500'
              }`}
            >
              上传文档
            </button>
            <button
              onClick={() => setCurrentView('map')}
              disabled={!currentDocument}
              className={`py-4 px-2 border-b-2 ${
                currentView === 'map'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500'
              } disabled:opacity-50`}
            >
              知识地图
            </button>
            <button
              onClick={() => setCurrentView('qa')}
              disabled={!currentDocument}
              className={`py-4 px-2 border-b-2 ${
                currentView === 'qa'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500'
              } disabled:opacity-50`}
            >
              智能问答
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {currentView === 'upload' && (
          <UploadFile onDocumentUploaded={handleDocumentUploaded} />
        )}
        {currentView === 'map' && currentDocument && (
          <KnowledgeMap documentId={currentDocument} />
        )}
        {currentView === 'qa' && currentDocument && (
          <QAInterface documentId={currentDocument} />
        )}
      </main>
    </div>
  )
}

export default App
