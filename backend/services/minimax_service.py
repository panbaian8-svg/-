"""
MiniMax API service
支持 OCR、图片理解、文本生成
"""
import json
import traceback
import base64
from typing import Dict, Any, Optional
import httpx
from app.config import MINIMAX_API_KEY, MINIMAX_GROUP_ID, MINIMAX_MODEL, MINIMAX_BASE_URL, MOCK_MODE
from services.ai_provider import AIProvider


class MiniMaxService(AIProvider):
    """Service for interacting with MiniMax API"""

    def __init__(self):
        print(f"[MiniMax] Initializing, MOCK_MODE: {MOCK_MODE}")
        self.api_key = MINIMAX_API_KEY
        self.group_id = MINIMAX_GROUP_ID
        self.model = MINIMAX_MODEL
        self.base_url = MINIMAX_BASE_URL
        self.mock_mode = MOCK_MODE

    @property
    def provider_name(self) -> str:
        return "minimax"

    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """
        生成文本

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            **kwargs: 其他参数

        Returns:
            生成的文本
        """
        if self.mock_mode:
            return self._get_mock_response(user_prompt)

        try:
            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "group_id": self.group_id,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048)
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()

            # 检查 API 返回的错误
            if "base_resp" in result:
                status_code = result.get("base_resp", {}).get("status_code")
                status_msg = result.get("base_resp", {}).get("status_msg", "")
                if status_code or status_msg:
                    error_msg = f"{status_msg} (code: {status_code})"
                    # 检查余额不足
                    if "insufficient" in error_msg.lower() or "balance" in error_msg.lower() or status_code == 1008:
                        return "⚠️ MiniMax 账户余额不足，请充值或切换到 DeepSeek"
                    raise Exception(f"MiniMax API error: {error_msg}")

            # 检查响应是否有效
            if result.get("choices") and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                # API 返回了错误
                status_msg = result.get("base_resp", {}).get("status_msg", "Unknown error")
                raise Exception(f"MiniMax API error: {status_msg}")

        except Exception as e:
            print(f"[MiniMax] API error: {e}")
            # 检查是否是余额不足
            error_msg = str(e)
            if "insufficient balance" in error_msg or "1008" in error_msg or "balance" in error_msg.lower():
                return "⚠️ MiniMax 账户余额不足，请充值或切换到 DeepSeek"
            traceback.print_exc()
            return self._get_mock_response(user_prompt)

    def extract_knowledge(
        self,
        content: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        知识归纳

        Args:
            content: 文档内容
            **kwargs: 其他参数

        Returns:
            结构化的知识JSON
        """
        system_prompt = """你是一个专业的教育知识归纳专家，擅长将教材内容结构化提取。

你的任务是将给定的文本内容按照以下层级进行归纳：
1. 章节层级（Chapter）
2. 主题层级（Topic）
3. 公式层级（Formula）
4. 例题层级（Example）

输出格式要求：
- 必须是有效的 JSON 格式
- 每个层级包含 id、title、content
- 公式和例题要关联到对应的主题"""

        user_prompt = f"请对以下文本进行知识归纳：\n\n{content}"

        response = self.generate_text(system_prompt, user_prompt)

        try:
            # 尝试解析 JSON
            result = json.loads(response)
            # 规范化格式
            normalized = self._normalize_knowledge_format(result)
            if normalized:
                return normalized
            return result
        except json.JSONDecodeError:
            # 清理 markdown 代码块
            clean_response = response.strip()
            if clean_response.startswith("```"):
                lines = clean_response.split("\n")
                clean_lines = [l for l in lines if not l.strip().startswith("```")]
                clean_response = "\n".join(clean_lines).strip()
            try:
                result = json.loads(clean_response)
                normalized = self._normalize_knowledge_format(result)
                if normalized:
                    return normalized
                return result
            except:
                return self._get_mock_knowledge()

    def answer_question(
        self,
        question: str,
        context: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        问答

        Args:
            question: 问题
            context: 上下文/参考资料
            **kwargs: 其他参数

        Returns:
            答案和来源
        """
        if self.mock_mode:
            return {
                "answer": "MiniMax Mock: 这是问答功能的模拟响应",
                "sources": [{"content": context[:500] if context else ""}]
            }

        try:
            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            system_prompt = """你是一个智能助教，擅长根据提供的教材内容回答学生的问题。

请根据以下上下文内容回答用户的问题。
如果上下文中没有相关信息，请说明"我没有在教材中找到相关内容"。"""

            user_prompt = f"上下文：\n{context}\n\n问题：{question}"

            payload = {
                "model": self.model,
                "group_id": self.group_id,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2048
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()

            # 检查 API 返回的错误
            if "base_resp" in result:
                status_code = result.get("base_resp", {}).get("status_code")
                status_msg = result.get("base_resp", {}).get("status_msg", "")
                if status_code or status_msg:
                    error_msg = f"{status_msg} (code: {status_code})"
                    # 检查余额不足
                    if "insufficient" in error_msg.lower() or "balance" in error_msg.lower() or status_code == 1008:
                        return {
                            "answer": "⚠️ MiniMax 账户余额不足 (insufficient balance)，请充值或切换到 DeepSeek",
                            "sources": []
                        }
                    return {
                        "answer": f"MiniMax API 错误: {error_msg}",
                        "sources": []
                    }

            # 正常解析响应
            answer = result["choices"][0]["message"]["content"]

            return {
                "answer": answer,
                "sources": [{"content": context[:500] if context else ""}]
            }

        except Exception as e:
            error_msg = str(e)
            print(f"[MiniMax] answer_question error: {error_msg}")
            traceback.print_exc()
            # 检查是否是余额不足
            if "insufficient balance" in error_msg.lower() or "1008" in error_msg or "balance" in error_msg.lower():
                return {
                    "answer": "⚠️ MiniMax 账户余额不足 (insufficient balance)，请充值或切换到 DeepSeek",
                    "sources": []
                }
            # 检查是否是连接/API 错误
            return {
                "answer": f"⚠️ MiniMax 服务暂时不可用: {error_msg[:100]}",
                "sources": []
            }

    def support_ocr(self) -> bool:
        """MiniMax 支持 OCR"""
        return True

    def ocr_image(
        self,
        image_data: bytes,
        **kwargs
    ) -> str:
        """
        图片 OCR - 识别图片中的文字

        Args:
            image_data: 图片数据
            **kwargs: 其他参数

        Returns:
            识别出的文字
        """
        if self.mock_mode:
            return "这是图片中的文字（Mock OCR）"

        try:
            # 将图片转为 base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "group_id": self.group_id,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": "请识别图片中的所有文字并输出。"
                            }
                        ]
                    }
                ],
                "temperature": 0.3
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"[MiniMax] OCR error: {e}")
            traceback.print_exc()
            return ""

    def support_image_understanding(self) -> bool:
        """MiniMax 支持图片理解"""
        return True

    def understand_image(
        self,
        image_data: bytes,
        prompt: str = "",
        **kwargs
    ) -> str:
        """
        图片理解

        Args:
            image_data: 图片数据
            prompt: 提示词
            **kwargs: 其他参数

        Returns:
            图片描述/分析
        """
        if self.mock_mode:
            return "图片描述（Mock）"

        try:
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            if not prompt:
                prompt = "请详细描述这张图片的内容。"

            url = f"{self.base_url}/text/chatcompletion_v2"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "group_id": self.group_id,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                "temperature": 0.7
            }

            response = httpx.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"[MiniMax] Image understanding error: {e}")
            traceback.print_exc()
            return ""

    def _normalize_knowledge_format(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """规范化不同格式的响应到统一格式"""
        if isinstance(data, list):
            chapters = []
            for i, item in enumerate(data):
                chapter = {
                    "id": item.get("id", f"c{i+1}"),
                    "title": item.get("title", f"Chapter {i+1}"),
                    "content": item.get("content", ""),
                    "topics": []
                }
                chapters.append(chapter)
            return {"chapters": chapters}

        if "chapters" in data:
            return data

        if "knowledge_structure" in data:
            items = data.get("knowledge_structure", [])
            chapters = []
            for i, item in enumerate(items):
                chapter = {
                    "id": item.get("id", f"c{i+1}"),
                    "title": item.get("title", f"Chapter {i+1}"),
                    "content": item.get("content", ""),
                    "topics": []
                }
                chapters.append(chapter)
            return {"chapters": chapters}

        if "sections" in data:
            chapters = []
            course = data.get("course", "")
            unit = data.get("unit", "Unknown")
            chapters.append({
                "id": "c1",
                "title": unit,
                "content": course,
                "topics": []
            })
            for i, section in enumerate(data.get("sections", [])):
                topic = {
                    "id": f"t{i+1}",
                    "title": section.get("title", f"Section {i+1}"),
                    "content": section.get("definition", "") or str(section.get("types", [])),
                    "formulas": [],
                    "examples": []
                }
                chapters[0]["topics"].append(topic)
            return {"chapters": chapters}

        return None

    def _get_mock_response(self, user_prompt: str) -> str:
        """Mock 响应"""
        return json.dumps(self._get_mock_knowledge())

    def _get_mock_knowledge(self) -> Dict[str, Any]:
        """Mock 知识结构"""
        return {
            "chapters": [
                {
                    "id": "c1",
                    "title": "第一章",
                    "content": "这是 MiniMax Mock 数据",
                    "topics": []
                }
            ]
        }
