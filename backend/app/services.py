"""
Shared service instances
用于避免循环导入
"""
from services.knowledge_service import KnowledgeService
from services.rag_service import RAGService
from services.graph_service import GraphService

# Create singleton service instances
knowledge_service = KnowledgeService()
rag_service = RAGService()
graph_service = GraphService()
