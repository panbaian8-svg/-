import os
from dotenv import load_dotenv

# Load .env from backend directory
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path, override=True)

# ==================== AI 服务配置 ====================

# AI 提供商选择: "minimax" | "deepseek" | "both"
AI_PROVIDER = os.getenv("AI_PROVIDER", "deepseek")

# MiniMax 配置
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID", "")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "abab5.5-chat")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")

# DeepSeek 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# Mock 模式（API 不可用时使用测试数据）
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# ==================== 服务器配置 ====================
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# ==================== CORS 配置 ====================
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# ==================== 文件上传配置 ====================
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

# ==================== ChromaDB 配置 ====================
CHROMADB_PERSIST_DIR = os.getenv("CHROMADB_PERSIST_DIR", "./data/chroma")
