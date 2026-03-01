from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import traceback
from app.routers.documents import documents_db
from app.services import rag_service

router = APIRouter(prefix="/api/qa", tags=["qa"])


class AskRequest(BaseModel):
    question: str
    document_id: str
    top_k: int = 3


class AskResponse(BaseModel):
    answer: str
    sources: List[dict]
    related_topics: List[str]
    provider: str = "deepseek"
    source_type: str = "knowledge_base"  # "knowledge_base" or "ai_knowledge"


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    RAG-based question answering using DeepSeek
    """
    # Check if document exists
    if request.document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get document content
    document = documents_db[request.document_id]
    text_content = document.get("content", "")

    if not text_content:
        raise HTTPException(status_code=400, detail="Document has no content for Q&A")

    # Add document to vector store if not already
    try:
        # Check if document is already in vector store
        # For simplicity, we'll add it each time
        rag_service.add_document(request.document_id, text_content)

        # Get answer using RAG
        result = rag_service.answer_question(
            question=request.question,
            document_id=request.document_id,
            top_k=request.top_k
        )

        # Extract related topics from sources
        related_topics = []
        for source in result.get("sources", [])[:3]:
            # Simple extraction - in production, use NLP
            content = source.get("content", "")
            if len(content) > 50:
                related_topics.append(content[:50] + "...")

        return AskResponse(
            answer=result["answer"],
            sources=result["sources"],
            related_topics=related_topics if related_topics else ["相关知识点"],
            provider=result.get("provider", "deepseek"),
            source_type=result.get("source_type", "knowledge_base")
        )

    except Exception as e:
        # Fallback to mock response if RAG fails
        print(f"[QA Error] {str(e)}")
        traceback.print_exc()
        return AskResponse(
            answer=f"抱歉，处理您的问题时遇到了一些问题: {str(e)[:50]}",
            sources=[],
            related_topics=[]
        )
