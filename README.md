# StudyFlow AI - 智能助学系统

基于 AI 的智能教育辅助系统，支持文档上传、知识提取、知识地图可视化和智能问答。

## 功能特性

- 📄 **文档上传** - 支持 PDF 文档上传和解析
- 🧠 **知识提取** - AI 自动从文档中提取知识点
- 🗺️ **知识地图** - 可视化知识点之间的关系
- 💬 **智能问答** - 基于文档内容的问答系统
- 🔄 **AI 提供商切换** - 支持 DeepSeek 和 MiniMax 自由切换

## 技术栈

### 后端
- FastAPI
- Python
- ChromaDB (向量数据库)
- DeepSeek API / MiniMax API

### 前端
- React + TypeScript
- Vite
- Tailwind CSS
- Cytoscape.js (知识图谱可视化)

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd study-partner
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.docker .env

# 编辑 .env 文件，填入实际的 API Key
```

### 3. 本地运行

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

### 4. Docker 部署

```bash
# 构建并运行
docker-compose up -d
```

## API 文档

启动后端后访问: http://localhost:8000/docs

### 主要 API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/documents/upload` | POST | 上传 PDF 文档 |
| `/api/documents/ocr` | POST | 图片 OCR 识别 |
| `/api/documents/image/understand` | POST | 图片理解 |
| `/api/knowledge/extract` | POST | 提取知识 |
| `/api/knowledge/map` | GET | 获取知识地图 |
| `/api/knowledge/provider` | GET | 获取当前 AI 提供商 |
| `/api/knowledge/provider/switch` | POST | 切换 AI 提供商 |
| `/api/qa/ask` | POST | 智能问答 |

## 项目结构

```
study-partner/
├── backend/
│   ├── app/
│   │   ├── routers/      # API 路由
│   │   ├── config.py     # 配置
│   │   └── services.py   # 共享服务
│   ├── services/         # 业务逻辑
│   ├── main.py           # 应用入口
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React 组件
│   │   ├── api/         # API 客户端
│   │   └── App.tsx      # 主应用
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 配置说明

### DeepSeek
- 获取 API Key: https://platform.deepseek.com/
- 模型: deepseek-chat

### MiniMax
- 获取 API Key: https://platform.minimax.chat/
- Group ID: 从 MiniMax 控制台获取
- 模型: abab5.5-chat

## 许可证

MIT
