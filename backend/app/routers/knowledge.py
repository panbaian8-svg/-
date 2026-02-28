from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from app.routers.documents import documents_db
from app.services import knowledge_service, rag_service, graph_service

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

# In-memory storage for knowledge
knowledge_db = {}


class ProviderSwitchRequest(BaseModel):
    provider: str


@router.post("/provider/switch")
async def switch_provider(request: ProviderSwitchRequest):
    """
    切换 AI 提供商
    """
    allowed_providers = ["minimax", "deepseek"]
    if request.provider not in allowed_providers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid provider. Allowed: {allowed_providers}"
        )

    # Update services
    knowledge_service.set_provider(request.provider)
    rag_service.set_provider(request.provider)

    return {
        "status": "success",
        "provider": request.provider,
        "message": f"Switched to {request.provider}"
    }


@router.get("/provider")
async def get_provider():
    """
    获取当前 AI 提供商
    """
    return {
        "provider": knowledge_service.provider,
        "available_providers": ["minimax", "deepseek"]
    }


class ExtractRequest(BaseModel):
    document_id: str
    extraction_level: str = "chapter"


class KnowledgeResponse(BaseModel):
    knowledge_id: str
    document_id: str
    chapters: List[Dict[str, Any]]
    status: str


@router.post("/extract", response_model=KnowledgeResponse)
async def extract_knowledge(request: ExtractRequest):
    """
    Extract knowledge from document using DeepSeek API
    """
    # Check if document exists
    if request.document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get document content
    document = documents_db[request.document_id]
    text_content = document.get("content", "")

    if not text_content:
        raise HTTPException(status_code=400, detail="Document has no content to extract")

    # Limit text length for API (first 8000 characters)
    # DeepSeek has token limits
    text_to_process = text_content[:8000] if len(text_content) > 8000 else text_content

    # Extract knowledge using DeepSeek
    try:
        knowledge = knowledge_service.extract_knowledge(
            document_id=request.document_id,
            text=text_to_process,
            extraction_level=request.extraction_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge extraction failed: {str(e)}")

    knowledge_id = str(uuid.uuid4())

    # Store knowledge
    knowledge_db[knowledge_id] = {
        "knowledge_id": knowledge_id,
        "document_id": request.document_id,
        "chapters": knowledge.get("chapters", []),
        "status": "completed"
    }

    # Build knowledge graph
    graph_service.build_graph(knowledge)

    return KnowledgeResponse(
        knowledge_id=knowledge_id,
        document_id=request.document_id,
        chapters=knowledge.get("chapters", []),
        status="completed"
    )


@router.get("/map")
async def get_knowledge_map(document_id: str):
    """
    Get knowledge map (nodes and edges) for visualization
    """
    # Find knowledge for this document
    knowledge = None
    for k_id, k_data in knowledge_db.items():
        if k_data["document_id"] == document_id:
            knowledge = k_data
            break

    if not knowledge:
        # Return mock data if no knowledge extracted yet
        nodes = [
            {"id": "c1", "label": "第一章", "type": "chapter"},
            {"id": "t1", "label": "等待提取...", "type": "topic"}
        ]
        edges = [{"source": "c1", "target": "t1", "label": "包含"}]
        return {"nodes": nodes, "edges": edges}

    # Build graph from actual knowledge
    graph_service.build_graph({"chapters": knowledge["chapters"]})
    result = graph_service.get_nodes_and_edges()

    return result
