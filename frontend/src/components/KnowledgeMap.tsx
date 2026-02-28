import { useEffect, useState } from 'react'
import CytoscapeComponent_ from 'react-cytoscapejs'
const CytoscapeComponent = CytoscapeComponent_ as any
import api from '../api/client'

interface KnowledgeMapProps {
  documentId: string
}

interface Node {
  id: string
  label: string
  type: string
}

interface Edge {
  source: string
  target: string
  label?: string
}

interface CyElement {
  data: {
    id: string
    label: string
    type?: string
    source?: string
    target?: string
  }
}

export default function KnowledgeMap({ documentId }: KnowledgeMapProps) {
  const [elements, setElements] = useState<CyElement[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)

  useEffect(() => {
    const fetchKnowledgeMap = async () => {
      try {
        setLoading(true)
        const response = await api.get(`/knowledge/map?document_id=${documentId}`)
        const { nodes, edges } = response.data

        // Convert to Cytoscape format
        const cyElements: CyElement[] = [
          ...nodes.map((node: Node) => ({
            data: {
              id: node.id,
              label: node.label,
              type: node.type,
            },
          })),
          ...edges.map((edge: Edge) => ({
            data: {
              id: `${edge.source}-${edge.target}`,
              source: edge.source,
              target: edge.target,
              label: edge.label,
            },
          })),
        ]

        setElements(cyElements)
      } catch (err) {
        console.error('Failed to fetch knowledge map:', err)
        setError('加载知识地图失败')
      } finally {
        setLoading(false)
      }
    }

    if (documentId) {
      fetchKnowledgeMap()
    }
  }, [documentId])

  const stylesheet = [
    {
      selector: 'node',
      style: {
        'background-color': '#6b7280',
        'label': 'data(label)',
        'font-size': '12px',
        'color': '#374151',
        'text-valign': 'center',
        'text-halign': 'center',
      },
    },
    {
      selector: 'node[type="chapter"]',
      style: {
        'background-color': '#3b82f6',
        'font-size': '14px',
        'font-weight': 'bold',
      },
    },
    {
      selector: 'node[type="topic"]',
      style: {
        'background-color': '#10b981',
      },
    },
    {
      selector: 'node[type="formula"]',
      style: {
        'background-color': '#f59e0b',
        'shape': 'rectangle',
      },
    },
    {
      selector: 'node[type="example"]',
      style: {
        'background-color': '#8b5cf6',
        'shape': 'ellipse',
      },
    },
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#d1d5db',
        'target-arrow-color': '#d1d5db',
        'target-arrow-shape': 'triangle',
      },
    },
  ]

  const layout = {
    name: 'cose' as const,
    animate: true,
    fit: true,
    padding: 50,
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
        {error}
      </div>
    )
  }

  return (
    <div className="flex gap-4">
      {/* Knowledge Map */}
      <div className="flex-1 bg-white rounded-lg shadow-sm border p-4">
        <h2 className="text-lg font-semibold mb-4">知识地图</h2>
        <div className="h-[600px]">
          <CytoscapeComponent
            elements={elements as any}
            stylesheet={stylesheet}
            layout={layout}
            style={{ width: '100%', height: '100%' }}
            cy={(cy: any) => {
              cy.on('tap', 'node', (evt: any) => {
                const node = evt.target
                setSelectedNode({
                  id: node.id(),
                  label: node.data('label'),
                  type: node.data('type'),
                })
              })
            }}
          />
        </div>
      </div>

      {/* Node Info Panel */}
      {selectedNode && (
        <div className="w-64 bg-white rounded-lg shadow-sm border p-4">
          <h3 className="font-semibold mb-2">节点信息</h3>
          <div className="space-y-2">
            <p><span className="font-medium">类型：</span>{selectedNode.type}</p>
            <p><span className="font-medium">名称：</span>{selectedNode.label}</p>
          </div>
          <button
            onClick={() => setSelectedNode(null)}
            className="mt-4 text-sm text-gray-500 hover:text-gray-700"
          >
            关闭
          </button>
        </div>
      )}
    </div>
  )
}
