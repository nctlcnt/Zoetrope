# AI 服务
# 封装 AI API 调用，用于文本分析、评论生成、情感分析等

from typing import Optional
from functools import lru_cache
import httpx

from ..config import settings


class AIServiceError(Exception):
    """AI 服务错误"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AIService:
    """
    AI 服务类

    使用 OpenAI 兼容 API 实现以下功能：
    - 文本总结和评论生成
    - Sentiment 分析（判断用户想看程度）
    - 从博文中提取标题、理由、信息
    - 文本 Embedding（用于向量检索）
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        embedding_model: str,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.embedding_model = embedding_model
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建 HTTP 客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=60.0,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self):
        """关闭 HTTP 客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # ========== 文本分析 ==========

    async def extract_media_info(self, text: str) -> dict:
        """
        从文本中提取媒体信息

        Args:
            text: 用户粘贴的博文/榜单文本

        Returns:
            {
                "titles": ["电影1", "电影2", ...],
                "comments": [{"title": "电影1", "comment": "评论内容", "sentiment": 0.8}, ...],
                "source_type": "blog" | "list" | "review"
            }

        TODO: 实现具体的 AI 调用逻辑
        """
        raise NotImplementedError("TODO: 实现媒体信息提取")

    async def analyze_sentiment(self, text: str) -> float:
        """
        分析文本的情感倾向

        Args:
            text: 评论或描述文本

        Returns:
            情感分数 (-1.0 到 1.0)
            - 负数：负面情感（不想看）
            - 0：中性
            - 正数：正面情感（想看）

        TODO: 实现具体的 AI 调用逻辑
        """
        raise NotImplementedError("TODO: 实现情感分析")

    async def generate_summary(self, media_title: str, comments: list[str]) -> str:
        """
        为媒体生成总结评论

        Args:
            media_title: 媒体标题
            comments: 相关评论列表

        Returns:
            AI 生成的总结文本

        TODO: 实现具体的 AI 调用逻辑
        """
        raise NotImplementedError("TODO: 实现总结生成")

    # ========== Embedding ==========

    async def get_embedding(self, text: str) -> list[float]:
        """
        获取文本的向量表示

        Args:
            text: 输入文本

        Returns:
            向量列表

        TODO: 实现具体的 AI 调用逻辑
        """
        raise NotImplementedError("TODO: 实现 Embedding 获取")

    async def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """
        批量获取文本的向量表示

        Args:
            texts: 输入文本列表

        Returns:
            向量列表的列表

        TODO: 实现具体的 AI 调用逻辑
        """
        raise NotImplementedError("TODO: 实现批量 Embedding 获取")


@lru_cache
def get_ai_service() -> AIService:
    """获取 AI 服务单例（依赖注入用）"""
    return AIService(
        api_key=settings.ai_api_key,
        base_url=settings.ai_api_base_url,
        model=settings.ai_model,
        embedding_model=settings.ai_embedding_model,
    )
