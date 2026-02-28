# StudyFlow AI 开发 Agent 指令

**生成时间：** 2026-03-02 03:00
**目标：** 在 09:00 前完成所有 P0 任务并提交代码
**当前项目完成度：** 65-70%
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

## 🔄 3 次尝试规则

遇到错误时，自动尝试修复（最多 3 次）：
1. 直接修复错误
2. 调整方案重试
3. 尝试替代实现

3 次都失败后，再询问用户。

---

## 📋 一、当前项目状态

### 已完成的功能
- ✅ 后端框架（FastAPI）
- ✅ AI 提供商抽象层（AIProvider、AIServiceSelector）
- ✅ MiniMax 服务（OCR、图片理解、文本生成、知识归纳、问答）
- ✅ 文档上传 API
- ✅ OCR API
- ✅ 图片理解 API
- ✅ 前端项目结构（React + Vite + Tailwind）
- ✅ 前端组件（UploadFile、KnowledgeMap、QAInterface、ProviderSelector）
- ✅ 配置管理（.env 完整）

### 未完成的功能
- ❌ 知识地图 API（GET /api/knowledge/map）
- ❌ 知识归纳 API（POST /api/knowledge/extract）
- ❌ RAG 问答 API（POST /api/qa/ask，包含 ChromaDB 集成）
- ❌ 前端 API 集成
- ❌ ProviderSelector 完整功能

---

## 🎯 二、开发计划（03:00-09:00）

### 阶段 1：API 完善（03:00-04:00）

#### 任务 1：实现知识地图 API（03:00-03:30）
**优先级：** P0
**文件：** `backend/app/routers/knowledge.py`
**要求：**
- 实现 GET /api/knowledge/map?document_id={id}
- 返回格式：`{"nodes": [...], "edges": [...]}`
- 调用 `GraphService` 构建知识图谱
- 添加错误处理

**验证方式：**
```bash
curl http://localhost:8000/api/knowledge/map?document_id=test-id
```

#### 任务 2：实现知识归纳 API（03:30-04:00）
**优先级：** P0
**文件：** `backend/app/routers/knowledge.py`
**要求：**
- 实现 POST /api/knowledge/extract
- 请求格式：`{"document_id": "uuid", "extraction_level": "chapter"}`
- 返回格式：`{"knowledge_id": "uuid", "chapters": [...], "status": "completed"}`
- 调用 `KnowledgeService` 和 AI 服务进行知识归纳
- 集成 MiniMax/DeepSeek（通过 AIServiceSelector）

**验证方式：**
```bash
curl -X POST http://localhost:8000/api/knowledge/extract \
  -H "Content-Type: application/json" \
  -d '{"document_id": "test-id", "extraction_level": "chapter"}'
```

---

### 阶段 2：RAG 问答（04:00-05:00）

#### 任务 3：实现 RAG 问答 API（04:00-04:45）
**优先级：** P0
**文件：** `backend/app/routers/qa.py`
**要求：**
- 实现 POST /api/qa/ask
- 请求格式：`{"question": "...", "document_id": "uuid", "top_k": 3}`
- 返回格式：`{"answer": "...", "sources": [...], "related_topics": [...]}`
- 集成 ChromaDB 进行向量存储和检索
- 使用 AI 服务生成答案
- 添加错误处理和超时机制

**验证方式：**
```bash
curl -X POST http://localhost:8000/api/qa/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是函数？", "document_id": "test-id", "top_k": 3}'
```

#### 任务 4：测试 AI 服务集成（04:45-05:00）
**优先级：** P0
**要求：**
- 测试 MiniMax 服务调用
- 测试 DeepSeek 服务调用（如果可用）
- 验证 AIServiceSelector 切换功能
- 确认 MOCK_MODE 正常工作

**验证方式：**
- 调用 MiniMax API 并检查响应
- 切换到 DeepSeek 并验证

---

### 阶段 3：前后端联调（05:00-06:00）

#### 任务 5：前端 UploadFile 组件 API 集成（05:00-05:30）
**优先级：** P0
**文件：** `frontend/src/components/UploadFile.tsx`
**要求：**
- 使用 axios 调用 /api/documents/upload
- 处理上传进度
- 显示文档信息（ID、页数、字数）
- 错误处理和用户提示
- 上传成功后触发文档 ID 回调

#### 任务 6：前端 KnowledgeMap 和 QAInterface 集成（05:30-06:00）
**优先级：** P0
**文件：**
- `frontend/src/components/KnowledgeMap.tsx`
- `frontend/src/components/QAInterface.tsx`
**要求：**
- KnowledgeMap：调用 /api/knowledge/map，使用 Cytoscape.js 渲染
- QAInterface：调用 /api/qa/ask，展示答案和来源
- 加载状态显示
- 错误处理

---

### 🍽️ 阶段 4：休息与评估（06:00-06:30）

#### 任务 7：休息 + 进度评估
**说明：**
- 吃早餐/休息
- 评估当前完成度
- 调整后续计划（如有必要）

---

### 阶段 5：ProviderSelector 完善（06:30-07:30）

#### 任务 8：ProviderSelector 后端 API（06:30-07:00）
**优先级：** P1
**文件：** `backend/app/routers/config.py`（新建）
**要求：**
- 实现 POST /api/config/provider
- 请求格式：`{"provider": "minimax" | "deepseek"}`
- 更新 AI_PROVIDER 配置
- 返回当前提供商状态

#### 任务 9：ProviderSelector 前端功能（07:00-07:30）
**优先级：** P1
**文件：** `frontend/src/components/ProviderSelector.tsx`
**要求：**
- 实现下拉选择器
- 调用 /api/config/provider API
- 显示当前提供商
- 切换后刷新页面以应用新配置

---

### 阶段 6：端到端测试（07:30-08:30）

#### 🚨 任务 10：端到端完整流程测试（07:30-08:00）
**优先级：** P0
**⚠️ 重要：必须使用浏览器自动测试**

**要求：**
1. 使用 Playwright MCP 启动浏览器
2. 自动化执行以下流程：
   - 打开 http://localhost:5173
   - 上传测试 PDF 文件
   - 等待知识归纳完成
   - 切换到知识地图页面，验证节点显示
   - 切换到问答页面，输入测试问题
   - 验证答案和来源显示

3. 使用 Web Reader MCP 验证页面内容
4. 使用 Zai MCP 进行截图对比（如有预期 UI）

**MCP 工具要求：**
- ✅ 使用 `Playwright` 进行浏览器自动化
- ✅ 使用 `Web Reader` 读取页面内容
- ✅ 使用 `Zai MCP` 进行 UI 截图对比

**测试脚本示例：**
```python
# 使用 Playwright MCP
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. 打开页面
    page.goto("http://localhost:5173")
    page.screenshot(path="screenshot_1_home.png")

    # 2. 上传文件
    page.set_input_files("input[type='file']", "test.pdf")
    page.click("button[type='submit']")
    page.wait_for_timeout(5000)

    # 3. 切换到知识地图
    page.click("text=知识地图")
    page.wait_for_selector(".cytoscape-container")
    page.screenshot(path="screenshot_2_map.png")

    # 4. 切换到问答
    page.click("text=智能问答")
    page.fill("input[placeholder='输入问题']", "什么是函数？")
    page.click("button[type='submit']")
    page.wait_for_timeout(3000)
    page.screenshot(path="screenshot_3_qa.png")

    browser.close()
```

#### 任务 11：测试 OCR 功能（08:00-08:15）
**优先级：** P1
**要求：**
- 上传测试图片
- 调用 /api/documents/ocr
- 验证文字识别正确性
- 使用 Zai MCP `extract_text_from_screenshot` 进行对比

#### 任务 12：测试图片理解（08:15-08:30）
**优先级：** P1
**要求：**
- 上传测试图片
- 调用 /api/documents/image/understand
- 验证图片描述正确性

---

### 阶段 7：提交准备（08:30-09:00）

#### 任务 13：修复发现的 bug（08:30-08:50）
**优先级：** P0
**要求：**
- 修复测试中发现的 bug
- 优先级顺序：阻断性 > 严重性 > 一般性

#### 任务 14：Git 提交和推送（08:50-09:00）
**优先级：** P0 ⚠️ 必须完成
**要求：**
```bash
cd /Users/yifanshi/Desktop/study-partner
git add .
git commit -m "feat: 完成 P0 核心功能

- 实现知识地图 API
- 实现知识归纳 API
- 实现 RAG 问答 API（ChromaDB 集成）
- 前后端联调完成
- 端到端测试通过"
git push origin main
```

---

## 📊 三、任务执行规范

### 任务标记格式
每个任务使用以下状态：
- `[ ]` 未开始
- `[~]` 进行中
- `[x]` 已完成
- `[!]` 有风险/阻塞

### 任务完成存档格式
每个任务完成后，生成以下存档：

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
| backend/app/routers/knowledge.py | 添加知识地图和归纳 API |
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

### 进度追踪
使用 `TaskCreate` 和 `TaskUpdate` 工具管理任务：
1. 开始任务时：`TaskUpdate(taskId=..., status="in_progress")`
2. 完成任务时：`TaskUpdate(taskId=..., status="completed")`

---

## 🔍 四、MCP 工具使用规范

### 必须使用 MCP 的场景

#### 1. API 测试（所有 API）
```python
# 使用 Playwright/Fetch MCP
POST http://localhost:8000/api/documents/upload
POST http://localhost:8000/api/knowledge/extract
GET http://localhost:8000/api/knowledge/map?document_id=xxx
POST http://localhost:8000/api/qa/ask
```

#### 2. 前端测试（所有前端功能）
```python
# 使用 Web Reader MCP
GET http://localhost:5173

# 使用 Playwright MCP（浏览器自动化）
- 页面加载验证
- 组件渲染验证
- 用户交互验证
```

#### 3. 🚨 端到端测试（必须使用浏览器）
```python
# 使用 Playwright MCP
1. 启动浏览器（非 headless 模式，便于调试）
2. 打开前端页面
3. 执行完整用户流程
4. 截图保存关键步骤

# 使用 Web Reader MCP
1. 验证页面 HTML 结构
2. 检查关键元素是否存在

# 使用 Zai MCP（可选）
1. 对比 UI 截图
2. OCR 文字识别验证
```

#### 4. OCR 测试
```python
# 使用 Zai MCP: extract_text_from_screenshot
# 对比识别结果
```

### 测试时机
- ✅ 每个任务完成后**立即测试**
- ✅ 不要等待所有任务完成再测试
- ✅ 失败时提供修复方案，不要只报告问题

---

## ⚠️ 五、重要注意事项

### 1. 稳定性要求
- ✅ 在现有代码基础上增量添加
- ❌ 不要大规模重构
- ✅ 每个改动后立即测试

### 2. 非开发职责（自动模式下）
- ❌ 不做技术选型决策
- ❌ 不做功能优先级判断
- ❌ 不做重大架构修改
- ✅ 遇到非重大问题，自动修复并继续
- ✅ 只在重大问题时使用 AskUserQuestion 询问

### 2.1 重大问题定义（必须询问）
- 🔴 需要选择新的技术栈（如 React vs Vue）
- 🔴 需要删除计划中的 P0 功能
- 🔴 涉及 API Key、密码等敏感信息
- 🔴 计划中的任务无法按时完成
- 🔴 需要大幅重构现有代码

### 2.2 正常问题定义（自动处理）
- ✅ 代码语法错误（修复语法）
- ✅ 导入缺失（添加导入）
- ✅ 参数错误（修正参数）
- ✅ 路径错误（修正路径）
- ✅ API 调用失败（调整参数/重试）
- ✅ 测试失败（分析日志并修复）

### 3. 时间管理
- ⏰ 严格遵守时间段
- 🚨 08:50 必须开始 Git 提交
- 🚨 09:00 必须完成提交

### 4. 🚨 关键要求：浏览器自动化测试
**在执行任务 10（端到端测试）时：**
- ✅ 必须使用 Playwright MCP 启动浏览器
- ✅ 必须自动化执行完整用户流程
- ✅ 必须截图保存关键步骤
- ❌ 不能只手动测试，必须自动化

**浏览器测试示例代码：**
```javascript
// Playwright 自动化测试脚本
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,  // 非无头模式，便于调试
    slowMo: 500      // 慢速执行，便于观察
  });

  const page = await browser.newPage();

  try {
    // 1. 访问首页
    await page.goto('http://localhost:5173');
    await page.screenshot({ path: 'test_01_home.png' });
    console.log('✅ 首页加载成功');

    // 2. 上传文件
    const fileInput = await page.$('input[type="file"]');
    if (fileInput) {
      await fileInput.setInputFiles('/Users/yifanshi/Desktop/study-partner/test.pdf');
      console.log('✅ 文件选择成功');
    }

    // 3. 提交上传
    await page.click('button[type="submit"]');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: 'test_02_upload_result.png' });
    console.log('✅ 文件上传成功');

    // 4. 切换到知识地图
    await page.click('text=知识地图');
    await page.waitForSelector('.cytoscape-container', { timeout: 10000 });
    await page.screenshot({ path: 'test_03_knowledge_map.png' });
    console.log('✅ 知识地图渲染成功');

    // 5. 切换到问答
    await page.click('text=智能问答');
    await page.waitForSelector('textarea', { timeout: 5000 });
    await page.screenshot({ path: 'test_04_qa_page.png' });
    console.log('✅ 问答页面加载成功');

    // 6. 输入问题
    await page.fill('textarea', '什么是函数？');
    await page.screenshot({ path: 'test_05_question_input.png' });

    // 7. 提交问题
    await page.click('button[type="submit"]');
    await page.waitForTimeout(5000);
    await page.screenshot({ path: 'test_06_answer_result.png' });
    console.log('✅ 问答成功');

    // 8. 验证答案显示
    const answer = await page.$('.answer-content');
    if (answer) {
      const answerText = await answer.textContent();
      console.log('✅ 答案显示成功:', answerText.substring(0, 100));
    }

  } catch (error) {
    console.error('❌ 测试失败:', error);
    await page.screenshot({ path: 'test_error.png' });
  } finally {
    await browser.close();
  }
})();
```

---

## 📝 六、报告格式

### 每个阶段完成后报告

```markdown
## [阶段名称] 完成报告

### 已完成任务
- [x] 任务 1: [任务名]
- [x] 任务 2: [任务名]

### 遇到的问题
[如有问题，详细说明]

### 解决方案
[如何解决的]

### 下一步
[下一个阶段]
```

### 最终完成报告（09:00）

```markdown
## 🎯 StudyFlow AI 开发完成报告

### 任务完成情况
- 总任务数: 14
- 已完成: [数量]
- 失败/阻塞: [数量]
- 完成率: [%]

### P0 功能状态
| P0 功能 | 状态 | 说明 |
|---------|------|------|
| 知识地图 API | ✅ / ❌ | ... |
| 知识归纳 API | ✅ / ❌ | ... |
| RAG 问答 API | ✅ / ❌ | ... |
| 前端集成 | ✅ / ❌ | ... |
| 端到端测试 | ✅ / ❌ | ... |

### Git 提交状态
- 提交完成: ✅ / ❌
- 推送完成: ✅ / ❌
- Commit SHA: [如适用]

### 遗留问题
[如有未解决的问题]

### 建议后续优化
[演示后可以优化的地方]
```

---

## 🚀 七、开始执行（自动模式）

### 步骤 1：创建任务列表
使用 `TaskCreate` 创建所有 14 个任务

### 步骤 2：按顺序自动执行
从任务 1 开始，逐个完成：
- 每个任务自动执行，不需要询问
- 遇到正常问题自动修复（最多 3 次尝试）
- 3 次尝试都失败才询问用户

### 步骤 3：每个任务完成后
1. 使用 MCP 工具进行测试
2. 生成任务完成存档
3. 更新任务状态为 `completed`
4. **直接开始下一个任务，不需要等待用户确认**

### 步骤 4：遇到阻塞时（仅重大问题）
- 判断是否属于重大问题（见上方 2.1 定义）
- 如果是，使用 `AskUserQuestion` 询问用户
- 如果不是，继续自动尝试修复

### 🚀 自动执行示例

**示例 1：正常问题（自动修复）**
```
❌ 错误：ModuleNotFoundError: No module named 'chromadb'
✅ 自动修复：pip install chromadb
✅ 修复成功，继续执行
```

**示例 2：重大问题（询问用户）**
```
❌ 错误：计划中的知识地图功能需要额外 1 小时
🔴 这是重大问题（任务无法按时完成）
📋 使用 AskUserQuestion 询问用户
```

### ⏰ 自动报告进度

每个任务完成后，自动报告：
```markdown
✅ 任务完成
- 任务: [任务名]
- 用时: [时间]
- 状态: 自动执行
- 下一步: [下一个任务]
```

---

**最后更新：** 2026-03-02 03:00
**生成者：** 用户指令
**执行者：** 开发 Agent

---

> ⚠️ **关键提醒：** 在任务 10（端到端测试）时，必须使用 Playwright MCP 启动浏览器进行自动化测试，并保存截图！
