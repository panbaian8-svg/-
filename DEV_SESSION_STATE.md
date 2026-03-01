# StudyFlow AI - 开发会话状态

**最后更新：** 2026-03-02 06:30
**比赛截止：** 2026-03-02 09:00
**剩余时间：** 约 2.5 小时

---

## 🎯 核心任务

**目标：** 在 09:00 前完成前端界面优化并适配后端

**策略：**
- 🎨 前端先行：从"前端3.4"复制 UI 设计
- 🔌 后端适配：前端调用已存在的后端 API
- ✅ 保留知识地图：不删除现有功能，只优化 UI

---

## 📋 详细任务列表（共 11 个任务）

### 阶段 1：环境准备与设计迁移（30 分钟）

#### [ ] 任务 1：安装 shadcn/ui 依赖（10 分钟）
**优先级：** P0
**文件：** `frontend/package.json`
**命令：**
```bash
cd /Users/yifanshi/Desktop/study-partner/frontend
npm install lucide-react react-router-dom clsx tailwind-merge class-variance-authority
npx shadcn@latest add button input textarea scroll-area badge
npx shadcn@latest add dialog alert dropdown-menu
npx shadcn@latest add card tabs progress
```

#### [ ] 任务 2：迁移参考设计到项目（20 分钟）
**优先级：** P0
**源路径：** `/Users/yifanshi/Desktop/前端3.4/src/`
**目标路径：** `/Users/yifanshi/Desktop/study-partner/frontend/src/`

**需要复制的文件：**
| 源文件 | 目标文件 | 说明 |
|---------|-----------|------|
| `App.tsx` | `frontend/src/App.tsx` | 路由结构（添加 ChatPage 和 KnowledgeBasePage） |
| `pages/ChatPage.tsx` | `frontend/src/pages/ChatPage.tsx` | 聊天页面（替换 QAInterface） |
| `pages/KnowledgeBasePage.tsx` | `frontend/src/pages/KnowledgeBasePage.tsx` | 知识库页面（替换 UploadFile） |
| `index.css` | `frontend/src/index.css` | 全局样式（Tailwind CSS 变量） |
| `lib/utils.ts` | `frontend/src/lib/utils.ts` | 工具函数（新建） |

**保留元素：**
- ✅ StudyFlow AI 品牌名称和 Logo
- ✅ 现有 KnowledgeMap 组件（不删除）
- ✅ ProviderSelector 组件（保留）

**需要新增的：**
- 🌐 双语言切换（CN/EN）
- 🖼️ 图片上传功能（聊天中）
- 📄 Word 文档上传（知识库中）

---

### 阶段 2：API 适配与集成（45 分钟）

#### [ ] 任务 3：适配后端 RAG 问答 API（25 分钟）
**优先级：** P0
**文件：** `frontend/src/pages/ChatPage.tsx`
**API 端点：** `POST /api/qa/ask`

**请求格式：**
```typescript
{
  question: string,
  document_id: string,
  top_k: number = 3
}
```

**响应格式：**
```typescript
{
  answer: string,
  sources: [{ content: string, ... }],
  related_topics: string[],
  provider: string
}
```

**修改点：**
- 将 mock 的 `setTimeout` 响应替换为真实 axios 调用
- 使用 `api.post('/api/qa/ask', { ... })`
- 显示来源信息（sources）
- 显示提供商信息（provider）
- 添加加载状态和错误处理

#### [ ] 任务 4：适配文档管理 API（20 分钟）
**优先级：** P0
**文件：** `frontend/src/pages/KnowledgeBasePage.tsx`
**API 端点：**
- `GET /api/documents/` - 获取文档列表
- `POST /api/documents/upload` - 上传文档
- `DELETE /api/documents/{id}` - 删除文档（如需要）

**修改点：**
- 将 mock 的 `mockDocuments` 替换为 API 调用
- 文档上传使用 FormData
- Word 文件验证（`.doc`, `.docx`）
- 上传成功后刷新文档列表

---

### 阶段 3：功能完善与优化（45 分钟）

#### [ ] 任务 5：完善双语言支持（15 分钟）
**优先级：** P1
**文件：** `ChatPage.tsx`, `KnowledgeBasePage.tsx`
**要求：**
- 确保中英文切换正常工作
- ChatPage 的 `translations` 对象完整
- KnowledgeBasePage 添加中英文文本
- 创建语言配置文件（可选）：`frontend/src/i18n/cn.ts`, `en.ts`

#### [ ] 任务 6：完善图片问答功能（15 分钟）
**优先级：** P1
**文件：** `ChatPage.tsx`
**API 端点：** `POST /api/documents/image/understand`

**流程：**
1. 用户上传图片 → 显示预览
2. 提交时调用图片理解 API
3. AI 返回图片描述
4. 将描述作为上下文发送给问答 API
5. 展示最终答案

#### [ ] 任务 7：优化 UI 细节（15 分钟）
**优先级：** P1
**文件：** 所有前端页面
**优化点：**
- 加载状态（Spinner/Shimmer 组件）
- 错误提示（Alert 组件）
- 成功提示（Toast/Sonner）
- 响应式布局（移动端适配）

---

### 阶段 4：测试与调试（30 分钟）

#### [ ] 任务 8：使用 Playwright MCP 测试前端功能（15 分钟）
**优先级：** P0
**⚠️ 必须使用浏览器自动化**

**测试流程：**
```python
# 启动浏览器
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. 打开首页
    page.goto("http://localhost:5173")
    page.screenshot(path="test_01_home.png")

    # 2. 切换语言
    page.click("text=中文")
    page.wait_for_timeout(500)
    page.screenshot(path="test_02_language.png")

    # 3. 切换到知识库
    page.click("text=知识库")
    page.wait_for_selector("input[type='file']", timeout=10000)
    page.screenshot(path="test_03_knowledge_base.png")

    # 4. 上传测试文档（如果有）
    # page.set_input_files("input[type='file']", "test.docx")

    # 5. 切换回问答页面
    page.goto("http://localhost:5173")
    page.screenshot(path="test_04_chat_page.png")

    # 6. 输入问题
    page.fill("textarea", "什么是函数？")
    page.screenshot(path="test_05_question_input.png")

    # 7. 提交问题
    page.click("button[type='submit']")
    page.wait_for_timeout(5000)
    page.screenshot(path="test_06_answer_result.png")

    browser.close()
```

**MCP 工具使用：**
- ✅ Playwright MCP - 浏览器自动化
- ✅ Web Reader MCP - 验证页面结构
- ✅ Zai MCP - OCR 验证（可选）

#### [ ] 任务 9：使用 Web Reader 验证前端结构（15 分钟）
**优先级：** P1
**验证项：**
- HTML 结构正确性
- 关键元素存在性
- 样式加载情况
- 路由跳转正常

---

### 阶段 5：修复与提交（15 分钟）

#### [ ] 任务 10：修复测试中发现的问题（10 分钟）
**优先级：** P0
**要求：**
- 根据测试结果修复 bug
- 优先级：阻断性 > 严重性 > 一般性

#### [ ] 任务 11：Git 提交和推送（5 分钟）
**优先级：** P0 ⚠️ 必须完成
**命令：**
```bash
cd /Users/yifanshi/Desktop/study-partner
git add .
git commit -m "feat: 完成前端界面优化

- 采用 shadcn/ui 设计风格
- 实现双语言支持（CN/EN）
- 集成 RAG 问答 API
- 集成文档管理 API
- 支持图片问答功能
- 端到端测试通过"
git push origin main
```

---

## 🎨 参考设计文件

**路径：** `/Users/yifanshi/Desktop/前端3.4/`

**设计特点：**
- 技术栈：React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui
- 颜色主题：indigo/violet 渐变
- 组件库：40+ shadcn/ui 组件
- 图标库：Lucide React

**关键页面：**
1. **ChatPage (`/`)**
   - 双语切换按钮
   - 图片上传按钮
   - 聊天消息区域（气泡样式）
   - 来源标注显示
   - 渐变色头像

2. **KnowledgeBasePage (`/knowledge-base`)**
   - Word 文档上传（拖拽）
   - 文档卡片网格布局
   - 搜索功能
   - 下载/删除操作

---

## 🔌 后端 API 状态

**所有 API 已实现，前端只需要集成！**

| API 端点 | 方法 | 功能 | 状态 |
|----------|------|------|------|
| `/api/documents/` | GET | 获取文档列表 | ✅ 已实现 |
| `/api/documents/upload` | POST | 上传文档 | ✅ 已实现 |
| `/api/documents/ocr` | POST | OCR 识别 | ✅ 已实现 |
| `/api/documents/image/understand` | POST | 图片理解 | ✅ 已实现 |
| `/api/qa/ask` | POST | RAG 问答 | ✅ 已实现 |
| `/api/knowledge/extract` | POST | 知识提取 | ✅ 已实现 |
| `/api/knowledge/map` | GET | 知识地图 | ✅ 已实现 |
| `/api/knowledge/provider/switch` | POST | 切换提供商 | ✅ 已实现 |
| `/api/knowledge/provider` | GET | 获取提供商 | ✅ 已实现 |

**后端运行命令：**
```bash
cd /Users/yifanshi/Desktop/study-partner/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**健康检查：** http://localhost:8000/health

---

## 📁 项目结构

**前端：** `/Users/yifanshi/Desktop/study-partner/frontend/`
- `src/App.tsx` - 主路由
- `src/components/` - 组件（UploadFile, KnowledgeMap, QAInterface, ProviderSelector）
- `src/pages/` - 页面（需要添加 ChatPage, KnowledgeBasePage）
- `src/lib/` - 工具函数（需要添加 utils.ts）
- `package.json` - 依赖配置

**后端：** `/Users/yifanshi/Desktop/study-partner/backend/`
- `main.py` - FastAPI 入口
- `app/routers/` - API 路由（documents, qa, knowledge）
- `app/services/` - 服务层（ai_provider, document_service, knowledge_service, rag_service, graph_service）
- `.env` - 环境变量（AI API Keys）

---

## ⚠️ 重要注意事项

### 1. 保留知识地图模块
- ✅ `KnowledgeMap.tsx` 组件已存在
- ✅ 后端 `/api/knowledge/map` API 已实现
- 🎯 只优化 UI，不删除功能

### 2. 自动执行规则
- ✅ 代码实现 - 自动执行
- ✅ Bug 修复 - 自动执行（最多 3 次尝试）
- ✅ 测试验证 - 自动执行
- ✅ Git 提交 - 自动执行
- 🔴 重大决策 - 必须询问用户

### 3. 重大问题定义
- 需要选择新技术栈
- 需要删除 P0 功能
- 涉及 API Key 或敏感信息
- 计划无法按时完成
- 需要大幅重构

### 4. 正常问题定义
- 依赖安装失败
- API 调用错误
- 代码语法错误
- 路径错误
- 测试失败

---

## 🔄 新对话启动指南

### 重启后，使用以下指令：

```
请读取并执行 /Users/yifanshi/Desktop/study-partner/DEV_SESSION_STATE.md
```

### 或者更简洁：

```
加载 StudyFlow AI 开发会话状态
```

### 我会自动：
1. 读取本文件（`DEV_SESSION_STATE.md`）
2. 了解所有 11 个任务的详情
3. 了解后端 API 状态
4. 了解参考设计路径
5. 开始执行任务 1（不询问，直接开始）
6. 每个任务完成后自动进行下一个
7. 使用 MCP 工具进行自动化测试
8. 遇到正常问题自动修复（3 次尝试）
9. 09:00 前完成 Git 提交和推送

---

## 📊 时间分配

| 阶段 | 时间 | 任务数 | 累计 |
|-------|------|-------|------|
| 阶段 1：环境准备 | 06:15-06:45 | 2 | 30 分钟 |
| 阶段 2：API 适配 | 06:45-07:30 | 2 | 45 分钟 |
| 阶段 3：功能完善 | 07:30-08:15 | 3 | 45 分钟 |
| 阶段 4：测试调试 | 08:15-08:45 | 2 | 30 分钟 |
| 阶段 5：修复提交 | 08:45-09:00 | 2 | 15 分钟 |

**总时间：** 2.75 小时
**当前时间：** 约 06:30
**截止时间：** 09:00

---

**最后更新：** 2026-03-02 06:30
**状态：** 等待开发 agent 执行

---

> 🚀 **重启后只需说：** "加载 StudyFlow AI 开发会话状态"
> 📋 **开发 agent 会自动读取本文件并开始工作**
