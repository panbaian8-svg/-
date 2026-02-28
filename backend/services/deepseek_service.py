"""
DeepSeek API service
"""
import json
import traceback
from typing import Optional, Dict, Any
from openai import OpenAI
from app.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MOCK_MODE


class DeepSeekService:
    """Service for interacting with DeepSeek API"""

    def __init__(self):
        print(f"[DeepSeek] Initializing with API Key: {DEEPSEEK_API_KEY[:10]}..., MOCK_MODE: {MOCK_MODE}")
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )
        self.mock_mode = MOCK_MODE

    @property
    def provider_name(self) -> str:
        return "deepseek"

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "deepseek-chat"
    ) -> str:
        """
        Send chat request to DeepSeek API

        Args:
            system_prompt: System prompt
            user_prompt: User prompt
            model: Model name

        Returns:
            Model response
        """
        print(f"[DeepSeek] chat called, mock_mode: {self.mock_mode}")

        if self.mock_mode:
            print("[DeepSeek] Using mock mode")
            return self._get_mock_response(user_prompt)

        try:
            print(f"[DeepSeek] Calling API with model: {model}")
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            result = response.choices[0].message.content
            print(f"[DeepSeek] API response (first 200 chars): {result[:200] if result else 'None'}")
            return result
        except Exception as e:
            print(f"[DeepSeek] API error: {e}")
            traceback.print_exc()
            return self._get_mock_response(user_prompt)

    def extract_knowledge(self, text: str) -> Dict[str, Any]:
        """
        Extract structured knowledge from text

        Args:
            text: Document text

        Returns:
            Structured knowledge JSON
        """
        print(f"[DeepSeek] extract_knowledge called with text length: {len(text)}")

        system_prompt = """你是一个专业的教育知识归纳专家，擅长将教材内容结构化提取。

你的任务是将给定的文本内容按照以下层级进行归纳：
1. 章节层级（Chapter）
2. 主题层级（Topic）
3. 公式层级（Formula）
4. 例题层级（Example）

输出格式要求：
- 必须是有效的 JSON 格式
- 每个层级包含 id、title、content、parent_id
- 公式和例题要关联到对应的主题"""

        user_prompt = f"请对以下文本进行知识归纳：\n\n{text}"

        response = self.chat(system_prompt, user_prompt)
        print(f"[DeepSeek] Response length: {len(response) if response else 0}")

        try:
            # Try to parse as JSON
            result = json.loads(response)
            print(f"[DeepSeek] Successfully parsed JSON")

            # Normalize to our expected format
            # DeepSeek may return different structures, convert to chapters format
            if "chapters" not in result:
                # Try to convert from other formats
                normalized = self._normalize_knowledge_format(result)
                if normalized:
                    return normalized

            return result
        except json.JSONDecodeError as e:
            print(f"[DeepSeek] JSON parse error: {e}")
            # Try to remove markdown code block markers
            clean_response = response.strip()
            if clean_response.startswith("```"):
                # Remove ```json and ```
                lines = clean_response.split("\n")
                clean_lines = [l for l in lines if not l.strip().startswith("```")]
                clean_response = "\n".join(clean_lines).strip()
                print(f"[DeepSeek] Attempting to parse cleaned response: {clean_response[:200]}...")
            try:
                result = json.loads(clean_response)
                print(f"[DeepSeek] Successfully parsed cleaned JSON")
                # Try to normalize
                normalized = self._normalize_knowledge_format(result)
                if normalized:
                    return normalized
                return result
            except:
                print(f"[DeepSeek] Still failed to parse, using mock")
                # Return mock structure if parsing fails
                return self._get_mock_knowledge()

    def _normalize_knowledge_format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize different API response formats to our chapters format"""

        # Handle array response (list of chapters/sections)
        if isinstance(data, list):
            # Convert array to chapters format
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

        # If already has chapters, return as is
        if "chapters" in data:
            return data

        # Handle knowledge_structure format
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

        # Try to convert from sections format
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
                    "content": section.get("definition", "") or section.get("types", []),
                    "formulas": [],
                    "examples": []
                }

                # Add types as formulas if present
                if "types" in section:
                    for j, t in enumerate(section["types"]):
                        topic["formulas"].append({
                            "id": f"f{j+1}",
                            "content": t,
                            "description": ""
                        })

                chapters[0]["topics"].append(topic)

            return {"chapters": chapters}

        return None

    def _get_mock_response(self, user_prompt: str) -> str:
        """Get mock response when API is unavailable"""
        print("[DeepSeek] Using mock response")
        return json.dumps(self._get_mock_knowledge())

    def _get_mock_knowledge(self) -> Dict[str, Any]:
        """Return mock knowledge structure"""
        return {
            "chapters": [
                {
                    "id": "c1",
                    "title": "第一章 函数",
                    "content": "本章介绍函数的基本概念和性质",
                    "topics": [
                        {
                            "id": "t1",
                            "title": "函数的定义",
                            "content": "函数是一种特殊的对应关系...",
                            "formulas": [
                                {
                                    "id": "f1",
                                    "content": "f(x) = y",
                                    "description": "函数的基本表示形式"
                                }
                            ],
                            "examples": [
                                {
                                    "id": "e1",
                                    "content": "求函数 f(x) = 2x + 1 在 x=3 时的值",
                                    "solution": "f(3) = 2*3 + 1 = 7"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
