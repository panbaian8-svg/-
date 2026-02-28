from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import uuid
from typing import Optional
import os
from services.document_service import DocumentService
from services.ai_provider import AIServiceSelector
from app.config import AI_PROVIDER

router = APIRouter(prefix="/api/documents", tags=["documents"])

# In-memory storage for documents (replace with database in production)
documents_db = {}
document_service = DocumentService()


class DocumentResponse(BaseModel):
    document_id: str
    title: str
    page_count: int
    text_length: int
    status: str


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), title: Optional[str] = None):
    """
    Upload and parse a PDF document
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    # Use filename as title if not provided
    if not title:
        title = file.filename.replace(".pdf", "")

    # Read file content
    content = await file.read()

    # Parse PDF with PyPDF2
    parsed = document_service.parse_pdf(content)

    if parsed["status"] == "error":
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {parsed.get('error')}")

    # Store document info with parsed content
    documents_db[document_id] = {
        "document_id": document_id,
        "title": title,
        "page_count": parsed["page_count"],
        "text_length": parsed["text_length"],
        "content": parsed["text"],
        "status": "completed"
    }

    return DocumentResponse(
        document_id=document_id,
        title=title,
        page_count=parsed["page_count"],
        text_length=parsed["text_length"],
        status="completed"
    )


@router.get("/{document_id}")
async def get_document(document_id: str):
    """
    Get document by ID
    """
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    return documents_db[document_id]


@router.get("/")
async def list_documents():
    """
    List all documents
    """
    return list(documents_db.values())


@router.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """
    OCR - 识别图片中的文字
    支持 PNG, JPG, JPEG 格式
    """
    # Check file type
    allowed_types = ["image/png", "image/jpeg", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Only image files (PNG, JPG, JPEG) are supported. Got: {file.content_type}"
        )

    # Read image data
    image_data = await file.read()

    # Check file size (max 10MB)
    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image file too large (max 10MB)")

    # Get AI service
    selector = AIServiceSelector(AI_PROVIDER)
    ai_service = selector.get_service()

    # Check if OCR is supported
    if not ai_service.support_ocr():
        raise HTTPException(
            status_code=400,
            detail=f"OCR is not supported by current provider: {ai_service.provider_name}"
        )

    # Perform OCR
    try:
        text = ai_service.ocr_image(image_data)
        return {
            "status": "success",
            "text": text,
            "provider": ai_service.provider_name,
            "file_size": len(image_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")


@router.post("/image/understand")
async def understand_image(
    file: UploadFile = File(...),
    prompt: Optional[str] = ""
):
    """
    图片理解 - 分析图片内容
    支持 PNG, JPG, JPEG 格式
    """
    # Check file type
    allowed_types = ["image/png", "image/jpeg", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Only image files (PNG, JPG, JPEG) are supported. Got: {file.content_type}"
        )

    # Read image data
    image_data = await file.read()

    # Check file size (max 10MB)
    if len(image_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image file too large (max 10MB)")

    # Get AI service
    selector = AIServiceSelector(AI_PROVIDER)
    ai_service = selector.get_service()

    # Check if image understanding is supported
    if not ai_service.support_image_understanding():
        raise HTTPException(
            status_code=400,
            detail=f"Image understanding is not supported by current provider: {ai_service.provider_name}"
        )

    # Perform image understanding
    try:
        description = ai_service.understand_image(image_data, prompt or "")
        return {
            "status": "success",
            "description": description,
            "provider": ai_service.provider_name,
            "file_size": len(image_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image understanding failed: {str(e)}")
