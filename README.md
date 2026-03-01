# StudyFlow AI - 智能助学系统

**HackTheEast 2026 参赛项目**

基于 AI 的智能教育辅助系统，支持文档上传、知识提取、知识地图可视化和智能问答。采用现代化 UI 设计（shadcn/ui），支持中英双语。

---

## 🌟 项目亮点

- 🎨 **现代化 UI** - 采用 shadcn/ui 组件库，渐变主题设计
- 🌐 **双语言支持** - 支持中文/English 界面切换
- 🖼️ **图片问答** - 支持图片上传 + 文本问答
- 🔄 **多 AI 提供商** - 支持 DeepSeek 和 MiniMax 切换
- ⚡ **RAG 检索** - 基于 ChromaDB 的向量检索和问答

---

## ✨ 功能特性

### 核心功能

| 功能 | 状态 | 说明 |
|-----|------|------|
| 📄 **文档上传** | ✅ 已实现 | 支持 PDF 文档上传和解析 |
| 🧠 **知识提取** | ✅ 已实现 | AI 自动从文档中提取知识点 |
| 🗺️ **知识地图** | ✅ 已实现 | 可视化知识点之间的关系 |
| 💬 **智能问答** | ✅ 已实现 | 基于文档内容的问答系统（RAG） |
| 🔍 **OCR 识别** | ✅ 已实现 | 识别图片中的文字 |
| 🖼️ **图片理解** | ✅ 已实现 | AI 分析图片内容并回答相关问题 |
| 🌐 **双语言** | ✅ 已实现 | 中英文界面切换 |
| 📁 **文档管理** | ✅ 已实现 | 知识库管理（查看、上传、删除） |

### 前端页面

- **ChatPage** (`/`) - 智能问答页面
  - 支持文本问答
  - 支持图片上传和问答
  - 双语言切换
  - shadcn/ui 现代设计

- **KnowledgeBasePage** (`/knowledge-base`) - 知识库管理页面
  - Word/PDF 文档上传
  - 文档列表展示
  - 文档搜索
  - 下载和删除功能

- **KnowledgeMap** - 知识地图可视化
  - 使用 Cytoscape.js 渲染
  - 节点和边可视化

- **UploadFile** - 文档上传（已由 KnowledgeBasePage 替代）

- **QAInterface** - 问答接口（已由 ChatPage 替代）

- **ProviderSelector** - AI 提供商切换

---

## 🛠️ 技术栈

### 后端

- **框架**：FastAPI
- **语言**：Python 3.13
- **数据库**：ChromaDB (向量数据库)
- **AI 服务**：
  - DeepSeek API (deepseek-chat 模型)
  - MiniMax API (abab5.5-chat 模型)
- **文档处理**：PyPDF2
- **向量检索**：RAG + ChromaDB

### 前端

- **框架**：React 19.2
- **语言**：TypeScript 5.9
- **构建工具**：Vite 7.2
- **样式**：Tailwind CSS 3.4
- **UI 组件**：shadcn/ui (40+ 可复用组件)
- **图标库**：Lucide React 0.562
- **路由**：React Router DOM 7.13
- **可视化**：Cytoscape.js (知识图谱)
- **HTTP 客户端**：Axios

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/panbaian8-svg/-.git
cd study-partner
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.docker .env

# 编辑 .env 文件，填入实际的 API Key
# 从以下平台获取：
# - DeepSeek: https://platform.deepseek.com/
# - MiniMax: https://platform.minimax.chat/
```

**环境变量说明：**
- `DEEPSEEK_API_KEY` - DeepSeek API Key
- `MINIMAX_API_KEY` - MiniMax API Key
- `MINIMAX_GROUP_ID` - MiniMax Group ID
- `AI_PROVIDER` - 当前使用的提供商 (deepseek 或 minimax)
- `MOCK_MODE` - 是否启用 Mock 模式 (true/false)

### 3. 安装依赖

#### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 前端
```bash
cd frontend
npm install
```

### 4. 本地运行

#### 后端
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问后端文档：http://localhost:8000/docs

#### 前端
```bash
cd frontend
npm run dev
```

访问前端：http://localhost:5173

### 5. Docker 部署（推荐）

```bash
# 构建并运行
docker-compose up -d
```

---

## 📡 API 文档

启动后端后访问：**http://localhost:8000/docs**

### 主要 API 端点

| 端点 | 方法 | 说明 |
|--------|------|------|
| `/api/documents/` | GET | 获取所有文档列表 |
| `/api/documents/upload` | POST | 上传 PDF/Word 文档 |
| `/api/documents/{document_id}` | GET | 获取指定文档详情 |
| `/api/documents/ocr` | POST | 图片 OCR 文字识别 |
| `/api/documents/image/understand` | POST | 图片内容理解和问答 |
| `/api/knowledge/extract` | POST | 提取文档知识结构 |
| `/api/knowledge/map` | GET | 获取知识地图数据 |
| `/api/knowledge/provider` | GET | 获取当前 AI 提供商 |
| `/api/knowledge/provider/switch` | POST | 切换 AI 提供商 |
| `/api/qa/ask` | POST | RAG 智能问答 |
| `/health` | GET | 健康检查 |

---

## 📁 项目结构

```
study-partner/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── routers/          # API 路由
│   │   │   ├── documents.py  # 文档 API
│   │   │   ├── qa.py          # 问答 API
│   │   │   └── knowledge.py   # 知识 API
│   │   ├── config.py          # 配置管理
│   │   └── main.py           # 应用入口
│   ├── services/              # 业务逻辑层
│   │   ├── ai_provider.py    # AI 提供商抽象
│   │   ├── deepseek_service.py # DeepSeek 服务
│   │   ├── minimax_service.py  # MiniMax 服务
│   │   ├── document_service.py # 文档解析
│   │   ├── rag_service.py     # RAG 问答
│   │   ├── knowledge_service.py # 知识提取
│   │   └── graph_service.py   # 知识图谱
│   ├── data/                 # ChromaDB 数据目录
│   ├── requirements.txt        # Python 依赖
│   ├── main.py              # FastAPI 入口
│   └── .env                 # 环境变量（需自行配置）
│
├── frontend/                # React 前端
│   ├── src/
│   │   ├── pages/           # 页面组件
│   │   │   ├── ChatPage.tsx           # 智能问答页面
│   │   │   ├── KnowledgeBasePage.tsx  # 知识库页面
│   │   │   ├── KnowledgeMap.tsx       # 知识地图
│   │   │   ├── UploadFile.tsx         # 上传组件
│   │   │   ├── QAInterface.tsx        # 问答接口（旧）
│   │   │   └── ProviderSelector.tsx    # 提供商选择
│   │   ├── components/      # 通用组件
│   │   │   ├── ui/       # shadcn/ui 组件
│   │   │   ├── KnowledgeMap.tsx
│   │   │   ├── ProviderSelector.tsx
│   │   │   ├── QAInterface.tsx
│   │   │   └── UploadFile.tsx
│   │   ├── lib/            # 工具函数
│   │   └── utils.ts      # 前端工具
│   ├── index.css           # 全局样式
│   ├── App.tsx             # 主应用（路由配置）
│   ├── main.tsx            # 入口文件
│   ├── package.json        # Node 依赖
│   ├── tsconfig.json       # TypeScript 配置
│   ├── tailwind.config.js   # Tailwind 配置
│   └── vite.config.ts      # Vite 配置
│
├── docker-compose.yml        # Docker 部署配置
├── .env.docker             # 环境变量模板
├── .gitignore             # Git 忽略文件
└── README.md              # 项目文档
```

---

## ⚙️ 配置说明

### DeepSeek
- **获取 API Key**: https://platform.deepseek.com/
- **模型**: `deepseek-chat`
- **文档**: https://platform.deepseek.com/docs/

### MiniMax
- **获取 API Key**: https://platform.minimax.chat/
- **获取 Group ID**: 从 MiniMax 控制台获取
- **模型**: `abab5.5-chat`
- **文档**: https://platform.minimax.chat/document/intro

### ChromaDB
- **向量存储**: 自动创建在 `backend/data/chroma/` 目录
- **自动清理**: 项目启动时会自动清理旧数据

---

## 🧪 测试

### 运行测试

```bash
# 后端测试
cd backend
pytest tests/

# 前端测试
cd frontend
npm test
```

### 健康检查

```bash
curl http://localhost:8000/health
```

---

## 📜 开发进度

### 已完成功能

- ✅ FastAPI 后端框架
- ✅ AI 提供商抽象层（AIServiceSelector）
- ✅ MiniMax 服务（OCR、图片理解、文本生成）
- ✅ DeepSeek 服务（文本生成、问答）
- ✅ 文档上传和解析
- ✅ ChromaDB 集成
- ✅ RAG 问答系统
- ✅ 知识提取 API
- ✅ 知识地图 API
- ✅ React + TypeScript 前端框架
- ✅ shadcn/ui 组件集成
- ✅ ChatPage 页面（双语言、图片问答）
- ✅ KnowledgeBasePage 页面（文档管理）
- ✅ KnowledgeMap 页面
- ✅ 响应式设计

### 待优化功能

- 🔄 知识地图 UI 风格统一
- 🔄 知识归纳功能的可视化展示
- 🔄 端到端测试自动化完善

---

## 🏆 比赛提交

### HackTheEast 2026

- **参赛作品**: StudyFlow AI - 智能助学系统
- **团队**: [您的团队名称]
- **GitHub**: https://github.com/panbaian8-svg/-
- **技术栈**: FastAPI, React, ChromaDB, DeepSeek/MiniMax

### 提交材料

- ✅ **源代码** - 已提交到 GitHub
- ✅ **README.md** - 完整的项目文档
- ✅ **Docker 配置** - docker-compose.yml
- ✅ **环境变量模板** - .env.docker
- ✅ **API 文档** - FastAPI 自动生成

---

## 📄 许可证

MIT License

---

## 👨 贡献者

- [您的团队成员]

---

**最后更新**: 2026-03-02 08:45

> 🎯 **项目目标**: 为学生提供基于 AI 的智能助学系统，提升学习效率
