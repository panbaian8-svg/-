"""
RAG (Retrieval-Augmented Generation) service
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from services.deepseek_service import DeepSeekService
from services.minimax_service import MiniMaxService
from services.document_service import DocumentService
from services.ai_provider import AIServiceSelector
from app.config import AI_PROVIDER


class RAGService:
    """Service for RAG-based question answering"""

    def __init__(self, provider: Optional[str] = None, persist_directory: str = "./data/chroma"):
        """
        初始化 RAG 服务

        Args:
            provider: AI 提供商 "minimax" | "deepseek"，默认使用配置
            persist_directory: ChromaDB 持久化目录
        """
        self.provider = provider or AI_PROVIDER
        self.selector = AIServiceSelector(self.provider)
        self.ai_service = self.selector.get_service()
        self.document_service = DocumentService()
        self.persist_directory = persist_directory
        self.client = None
        self.collections = {}
        print(f"[RAGService] Using AI provider: {self.provider}")

    def set_provider(self, provider: str):
        """
        切换 AI 提供商

        Args:
            provider: 新提供商 "minimax" | "deepseek"
        """
        self.provider = provider
        self.selector.switch_provider(provider)
        self.ai_service = self.selector.get_service()
        print(f"[RAGService] Switched to provider: {provider}")

    def _get_client(self):
        """Get or create ChromaDB client"""
        if self.client is None:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory
            )
        return self.client

    def create_collection(self, document_id: str):
        """
        Create a collection for a document

        Args:
            document_id: Document ID
        """
        client = self._get_client()
        collection_name = f"doc_{document_id}"
        collection = client.get_or_create_collection(name=collection_name)
        self.collections[document_id] = collection
        return collection

    def add_document(
        self,
        document_id: str,
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
    ):
        """
        Add document to vector store

        Args:
            document_id: Document ID
            text: Document text
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
        """
        # Create collection if not exists
        if document_id not in self.collections:
            self.create_collection(document_id)

        # Chunk text
        chunks = self.document_service.chunk_text(text, chunk_size, overlap)

        # TODO: Generate embeddings with DeepSeek
        # For now, use random embeddings (placeholder)
        import numpy as np
        embeddings = [[float(i) for i in np.random.rand(1536)] for _ in chunks]

        # Add to collection
        collection = self.collections[document_id]
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )

    def search(
        self,
        document_id: str,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks

        Args:
            document_id: Document ID
            query: Query string
            top_k: Number of results

        Returns:
            List of relevant chunks
        """
        if document_id not in self.collections:
            return []

        collection = self.collections[document_id]

        # TODO: Generate query embedding
        import numpy as np
        query_embedding = [float(i) for i in np.random.rand(1536)]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # Format results
        formatted_results = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                formatted_results.append({
                    "chunk_id": results["ids"][0][i],
                    "content": doc,
                    "distance": results["distances"][0][i] if "distances" in results else 0
                })

        return formatted_results

    def answer_question(
        self,
        question: str,
        document_id: str,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG

        Args:
            question: Question string
            document_id: Document ID
            top_k: Number of chunks to retrieve

        Returns:
            Answer and sources
        """
        # Retrieve relevant chunks
        sources = self.search(document_id, question, top_k)

        # Combine sources into context
        context = "\n\n".join([s["content"] for s in sources])

        # Generate answer with configured AI service
        result = self.ai_service.answer_question(question, context)

        return {
            "answer": result.get("answer", ""),
            "sources": sources,
            "provider": self.provider
        }
