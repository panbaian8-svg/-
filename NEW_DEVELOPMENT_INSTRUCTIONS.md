# StudyFlow AI 开发 Agent 指令 v2.0

**生成时间：** 2026-03-02 06:15
**目标：** 在 09:00 前完成前端界面优化并适配后端
**参考设计：** 桌面"前端3.4"项目
**模式：** 🚀 自动执行模式

---

## ⚠️ 自动执行模式说明

**你现在处于自动执行模式！**

以下情况**自动执行，不需要询问用户**：
- ✅ 代码实现
- ✅ Bug 修复
- ✅ 测试与验证
- ✅ 小问题调整
- ✅ Git 提交和推送
- ✅ 任务进度更新

以下情况**必须停止并询问用户**：
- 🔴 设计/架构决策
- 🔴 重大功能增删
- 🔴 安全/权限问题
- 🔴 API Key/敏感信息
- 🔴 计划无法完成

---

## 📊 一、项目当前状态

### 已完成的后端功能（无需修改）
- ✅ FastAPI 后端框架
- ✅ AI 提供商抽象层（MiniMax、DeepSeek）
- ✅ 文档上传 API
- ✅ OCR API
- ✅ 图片理解 API
- ✅ 配置管理

### 需要适配的后端功能
- 🔧 RAG 问答 API（POST /api/qa/ask）- 需适配前端 ChatPage
- 🔧 文档管理 API（上传、删除、列表）- 需适配 KnowledgeBasePage
- 🔧 图片问答 API（图片上传 + 文本问答）- 新增需求

### 前端现状
- 📁 原始前端：简单的白色卡片设计
- 🎨 目标设计：shadcn/ui 现代风格，双语支持，渐变主题

### 参考设计文件路径
```
/Users/yifanshi/Desktop/前端3.4/
```

---

## 🎯 二、开发计划（06:15-09:00）

### 阶段 1：环境准备与设计迁移（06:15-06:45）

#### 任务 1：安装 shadcn/ui 依赖（06:15-06:25）
**优先级：** P0
**文件：** `frontend/package.json`
**要求：**
- 安装必要的依赖：`radix-ui` 组件、`lucide-react`、`react-router-dom`
- 安装 `@tailwindcss/forms` 和 `tailwindcss-animate`
- 更新 Tailwind 配置

**验证方式：**
```bash
cd /Users/yifanshi/Desktop/study-partner/frontend
npm install lucide-react react-router-dom clsx tailwind-merge class-variance-authority
```

#### 任务 2：迁移参考设计到项目（06:25-06:45）
**优先级：** P0
**文件：**
- `frontend/src/App.tsx` - 更新路由
- `frontend/src/pages/ChatPage.tsx` - 新建，复制参考设计
- `frontend/src/pages/KnowledgeBasePage.tsx` - 新建，复制参考设计
- `frontend/src/index.css` - 更新全局样式
- `frontend/src/lib/utils.ts` - 新建，工具函数
**要求：**
- 从 `/Users/yifanshi/Desktop/前端3.4/src/` 复制核心页面设计
- 保留 StudyFlow AI 品牌元素（Logo、标题）
- 保留双语言切换功能（CN/EN）
- 保留图片上传功能
- 适配当前项目的 API 调用

---

### 阶段 2：API 适配与集成（06:45-07:30）

#### 任务 3：适配后端 RAG 问答 API（06:45-07:10）
**优先级：** P0
**文件：** `frontend/src/pages/ChatPage.tsx`
**要求：**
- 将 mock 的 AI 响应替换为真实的 `/api/qa/ask` 调用
- 实现以下 API 集成：
  ```typescript
  // 文本问答
  POST /api/qa/ask
  {
    "question": "用户问题",
    "document_id": "当前文档ID",
    "top_k": 3
  }
  -> { "answer": "...", "sources": [...] }

  // 图片问答
  POST /api/documents/image/understand
  {
    "image": "base64..."
  }
  -> { "description": "..." }
  ```
- 错误处理和加载状态显示
- 来源标注显示（sources）

#### 任务 4：适配文档管理 API（07:10-07:30）
**优先级：** P0
**文件：** `frontend/src/pages/KnowledgeBasePage.tsx`
**要求：**
- 替换 mock 文档列表为真实 API 调用
- 实现以下 API 集成：
  ```typescript
  // 获取文档列表
  GET /api/documents
  -> [{ "id": "...", "name": "...", "size": "...", "upload_date": "..." }]

  // 上传文档
  POST /api/documents/upload
  (FormData with file)
  -> { "document_id": "...", "message": "..." }

  // 删除文档
  DELETE /api/documents/{document_id}
  -> { "success": true }
  ```
- 实现 Word 文档上传验证
- 实现拖拽上传
- 错误处理

---

### 阶段 3：功能完善与优化（07:30-08:15）

#### 任务 5：完善双语言支持（07:30-07:45）
**优先级：** P1
**文件：** `frontend/src/pages/ChatPage.tsx`, `frontend/src/pages/KnowledgeBasePage.tsx`
**要求：**
- 完善 ChatPage 的中英文切换
- 完善 KnowledgeBasePage 的中英文切换
- 创建统一的语言配置文件（`frontend/src/i18n/`）

#### 任务 6：完善图片问答功能（07:45-08:00）
**优先级：** P1
**文件：** `frontend/src/pages/ChatPage.tsx`
**要求：**
- 图片上传预览
- 图片+文本同时发送给后端
- 后端返回图片描述 + 文本答案
- 聊天记录中显示图片

#### 任务 7：优化 UI 细节（08:00-08:15）
**优先级：** P1
**文件：** 所有前端页面
**要求：**
- 加载动画（shimmer/skeleton）
- 错误提示（Alert 组件）
- 成功提示（Toast/Sonner）
- 响应式优化

---

### 阶段 4：测试与调试（08:15-08:45）

#### 任务 8：使用 Playwright MCP 测试前端功能（08:15-08:30）
**优先级：** P0
**⚠️ 重要：必须使用浏览器自动测试**

**要求：**
1. 使用 Playwright MCP 启动浏览器
2. 自动化执行以下流程：
   - 打开 http://localhost:5173
   - 切换语言（中文 ↔ English）
   - 切换到知识库页面
   - 上传测试 Word 文档
   - 验证文档显示
   - 切换回问答页面
   - 输入测试问题
   - 验证答案显示
   - 上传测试图片
   - 验证图片+问答功能

3. 截图保存关键步骤

**MCP 工具要求：**
- ✅ 使用 `Playwright` 进行浏览器自动化
- ✅ 使用 `Web Reader` 读取页面内容
- ✅ 使用 `Zai MCP` 进行 OCR 测试验证

#### 任务 9：使用 Web Reader 验证前端结构（08:30-08:45）
**优先级：** P1
**要求：**
- 验证 HTML 结构正确性
- 验证关键元素存在性
- 验证样式加载
- 记录任何问题

---

### 阶段 5：修复与提交（08:45-09:00）

#### 任务 10：修复测试中发现的问题（08:45-08:55）
**优先级：** P0
**要求：**
- 根据测试结果修复 bug
- 优先级：阻断性 > 严重性 > 一般性

#### 任务 11：Git 提交和推送（08:55-09:00）
**优先级：** P0 ⚠️ 必须完成
**要求：**
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

## 📋 三、参考设计文件映射

### 从"前端3.4"复制的文件

| 源文件路径 | 目标文件路径 | 说明 |
|------------|--------------|------|
| `src/App.tsx` | `frontend/src/App.tsx` | 路由结构 |
| `src/pages/ChatPage.tsx` | `frontend/src/pages/ChatPage.tsx` | 聊天页面设计 |
| `src/pages/KnowledgeBasePage.tsx` | `frontend/src/pages/KnowledgeBasePage.tsx` | 知识库页面设计 |
| `src/index.css` | `frontend/src/index.css` | 全局样式 |
| `src/lib/utils.ts` | `frontend/src/lib/utils.ts` | 工具函数（新建）|

### shadcn/ui 组件（需要安装）

参考项目的 `src/components/ui/` 目录包含 40+ 组件，核心需要：
- Button, Input, Textarea, ScrollArea, Badge
- Dialog, Alert, DropdownMenu
- Card, Tabs, Progress

**安装方式：**
```bash
# 使用 shadcn-ui CLI
npx shadcn@latest add button input textarea scroll-area badge
npx shadcn@latest add dialog alert dropdown-menu
npx shadcn@latest add card tabs progress
```

---

## 🔍 四、MCP 工具使用规范

### 必须使用 MCP 的场景

#### 1. API 测试（所有 API）
```bash
# 使用 Playwright/Fetch MCP
POST http://localhost:8000/api/qa/ask
GET http://localhost:8000/api/documents
POST http://localhost:8000/api/documents/upload
```

#### 2. 前端测试（所有前端功能）
```bash
# 使用 Web Reader MCP
GET http://localhost:5173

# 使用 Playwright MCP（浏览器自动化）
- 页面加载验证
- 组件渲染验证
- 用户交互验证
```

#### 3. 🚨 端到端测试（必须使用浏览器）
```bash
# 使用 Playwright MCP
1. 启动浏览器（非 headless 模式）
2. 打开前端页面
3. 执行完整用户流程
4. 截图保存关键步骤

# 使用 Zai MCP（可选）
- OCR 文字识别验证
- UI 截图对比
```

---

## ⚠️ 五、重要注意事项

### 1. 🚨 保留知识地图模块
**根据团队讨论，知识地图模块应保留：**
- ✅ 这是已实现的核心功能
- ✅ 后端 API 已完成
- ✅ 前端组件已存在（`KnowledgeMap.tsx`）
- 🎯 可以在后续优化中完善 UI，但不要删除

### 2. 代码迁移原则
- 📁 从参考设计复制核心 UI 代码
- 🔌 保持与后端 API 的兼容性
- 🎨 保留 StudyFlow AI 品牌元素
- 🌐 完善双语言支持

### 3. API 适配原则
- 🔄 将 mock 数据替换为真实 API 调用
- ⚡ 使用 axios（项目已有）
- 🛡️ 添加错误处理和加载状态
- 📝 记录所有 API 端点

### 4. 非开发职责（自动模式下）
- ❌ 不做技术选型决策
- ❌ 不做功能优先级判断
- ❌ 不做重大架构修改
- ✅ 遇到非重大问题，自动修复并继续
- ✅ 只在重大问题时使用 AskUserQuestion 询问

### 5. 重大问题定义（必须询问）
- 🔴 需要选择新的技术栈（如换 UI 框架）
- 🔴 需要删除计划中的 P0 功能
- 🔴 涉及 API Key、密码等敏感信息
- 🔴 计划中的任务无法按时完成
- 🔴 需要大幅重构现有代码

### 6. 正常问题定义（自动处理）
- ✅ 依赖安装失败（重试/检查网络）
- ✅ API 调用错误（检查端点/参数）
- ✅ 样式问题（修正 CSS）
- ✅ 路由错误（检查路径）
- ✅ 类型错误（修正类型定义）

---

## 🔄 六、3 次尝试规则

遇到错误时，自动尝试修复（最多 3 次）：
1. 直接修复错误
2. 调整方案重试
3. 尝试替代实现

3 次都失败后，再询问用户。

---

## 📝 七、任务执行规范

### 任务标记格式
- `[ ]` 未开始
- `[~]` 进行中
- `[x]` 已完成
- `[!]` 有风险/阻塞

### 任务完成存档格式
```markdown
=== 任务完成存档 ===
任务ID: [任务编号]
任务名称: [任务名称]
完成时间: [YYYY-MM-DD HH:MM:SS]
实际耗时: [实际用时]

完成内容:
[具体做了什么]

产出文件:
| 文件路径 | 说明 |
|---------|------|
| frontend/src/pages/ChatPage.tsx | 聊天页面 |
| ... | ... |

验证结果:
- 测试方式: [Playwright / Curl / Web Reader]
- 测试结果: ✅ 通过 / ❌ 失败
- 响应时间: [ms]

风险/问题:
[记录任何风险或问题]

下一步任务:
- [ ] [依赖任务]
==================
```

---

## ⏰ 八、时间管理

| 时间节点 | 提醒内容 |
|---------|---------|
| 07:00 | "阶段 2 完成，继续阶段 3" |
| 08:00 | "阶段 3 完成，继续阶段 4" |
| 08:50 | "剩余 10 分钟，注意时间" |
| 08:55 | "最后 5 分钟，开始准备提交" |

---

## 🚀 九、开始执行（自动模式）

### 步骤 1：创建任务列表
使用 `TaskCreate` 创建所有 11 个任务

### 步骤 2：按顺序自动执行
从任务 1 开始，逐个完成

### 步骤 3：每个任务完成后
1. 使用 MCP 工具进行测试
2. 生成任务完成存档
3. 更新任务状态为 `completed`
4. **直接开始下一个任务**

### 步骤 4：遇到阻塞时（仅重大问题）
- 判断是否属于重大问题
- 如果是，使用 `AskUserQuestion` 询问用户
- 如果不是，继续自动尝试修复

---

**最后更新：** 2026-03-02 06:15
**生成者：** 开发 Agent
**参考设计：** 桌面"前端3.4"项目

---

> 🎨 **设计参考：** `/Users/yifanshi/Desktop/前端3.4`
> 🚀 **核心策略：** 前端先行，后端适配，保留知识地图模块
