"""
Knowledge extraction service
支持 MiniMax 和 DeepSeek 并行
"""
from typing import Dict, Any, List, Optional
from services.deepseek_service import DeepSeekService
from services.minimax_service import MiniMaxService
from services.document_service import DocumentService
from services.ai_provider import AIServiceSelector
from app.config import AI_PROVIDER


class KnowledgeService:
    """Service for extracting knowledge from documents"""

    def __init__(self, provider: Optional[str] = None):
        """
        初始化知识服务

        Args:
            provider: AI 提供商 "minimax" | "deepseek"，默认使用配置
        """
        self.provider = provider or AI_PROVIDER
        self.selector = AIServiceSelector(self.provider)
        self.ai_service = self.selector.get_service()
        self.document_service = DocumentService()
        print(f"[KnowledgeService] Using AI provider: {self.provider}")

    def set_provider(self, provider: str):
        """
        切换 AI 提供商

        Args:
            provider: 新提供商 "minimax" | "deepseek"
        """
        self.provider = provider
        self.selector.switch_provider(provider)
        self.ai_service = self.selector.get_service()
        print(f"[KnowledgeService] Switched to provider: {provider}")

    def extract_knowledge(
        self,
        document_id: str,
        text: str,
        extraction_level: str = "chapter"
    ) -> Dict[str, Any]:
        """
        Extract knowledge from document text

        Args:
            document_id: Document ID
            text: Document text
            extraction_level: Level of extraction (chapter/topic/formula/example)

        Returns:
            Structured knowledge
        """
        # Limit text length
        text_to_process = text[:8000] if len(text) > 8000 else text

        # Use configured AI service to extract knowledge
        knowledge = self.ai_service.extract_knowledge(text_to_process)

        # Add document ID
        if isinstance(knowledge, dict):
            knowledge["document_id"] = document_id
            knowledge["provider"] = self.provider

        return knowledge

    def get_knowledge_summary(self, knowledge: Dict[str, Any]) -> Dict[str, int]:
        """
        Get summary statistics of knowledge

        Args:
            knowledge: Knowledge structure

        Returns:
            Summary statistics
        """
        chapters = knowledge.get("chapters", [])
        topic_count = 0
        formula_count = 0
        example_count = 0

        for chapter in chapters:
            topics = chapter.get("topics", [])
            topic_count += len(topics)

            for topic in topics:
                formula_count += len(topic.get("formulas", []))
                example_count += len(topic.get("examples", []))

        return {
            "chapter_count": len(chapters),
            "topic_count": topic_count,
            "formula_count": formula_count,
            "example_count": example_count,
            "provider": self.provider
        }
