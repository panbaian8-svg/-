"""
AI Provider 抽象基类
定义统一的 AI 服务接口，支持 MiniMax 和 DeepSeek 并行
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class AIProvider(ABC):
    """AI 提供商抽象基类"""

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def support_ocr(self) -> bool:
        """
        是否支持 OCR

        Returns:
            True if OCR is supported
        """
        pass

    @abstractmethod
    def ocr_image(
        self,
        image_data: bytes,
        **kwargs
    ) -> str:
        """
        图片 OCR

        Args:
            image_data: 图片数据
            **kwargs: 其他参数

        Returns:
            识别出的文字
        """
        pass

    @abstractmethod
    def support_image_understanding(self) -> bool:
        """
        是否支持图片理解

        Returns:
            True if image understanding is supported
        """
        pass

    @abstractmethod
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
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        提供商名称

        Returns:
            提供商名称字符串
        """
        pass


class AIServiceSelector:
    """AI 服务选择器 - 根据配置选择对应的 AI 服务"""

    def __init__(self, provider: str = "deepseek"):
        """
        初始化选择器

        Args AI:
            provider: 提供商 "minimax" | "deepseek"
        """
        self.provider = provider
        self._service = None

    def get_service(self) -> AIProvider:
        """
        获取 AI 服务实例

        Returns:
            AIProvider 实现类
        """
        if self._service is not None:
            return self._service

        if self.provider == "minimax":
            from services.minimax_service import MiniMaxService
            self._service = MiniMaxService()
        elif self.provider == "deepseek":
            from services.deepseek_service import DeepSeekService
            self._service = DeepSeekService()
        else:
            # 默认使用 DeepSeek
            from services.deepseek_service import DeepSeekService
            self._service = DeepSeekService()

        return self._service

    def switch_provider(self, provider: str):
        """
        切换 AI 提供商

        Args:
            provider: 新提供商 "minimax" | "deepseek"
        """
        self.provider = provider
        self._service = None  # 清除缓存，，下次获取时重新创建
