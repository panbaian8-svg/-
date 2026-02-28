"""
Document parsing service
"""
import PyPDF2
from io import BytesIO
from typing import Dict, Any


class DocumentService:
    """Service for parsing PDF documents"""

    @staticmethod
    def parse_pdf(file_content: bytes) -> Dict[str, Any]:
        """
        Parse PDF content and extract text

        Args:
            file_content: PDF file bytes

        Returns:
            Dict containing text and metadata
        """
        try:
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            page_count = len(pdf_reader.pages)

            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return {
                "text": text,
                "page_count": page_count,
                "text_length": len(text),
                "status": "completed"
            }
        except Exception as e:
            return {
                "text": "",
                "page_count": 0,
                "text_length": 0,
                "status": "error",
                "error": str(e)
            }

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
        """
        Split text into chunks

        Args:
            text: Input text
            chunk_size: Size of each chunk
            overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap

        return chunks
