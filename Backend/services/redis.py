# Redis 缓存服务
# 用于缓存热度数据和会话管理

from typing import Optional, Any
from functools import lru_cache
import json

from ..config import settings


class RedisServiceError(Exception):
    """Redis 服务错误"""
    pass


class RedisService:
    """
    Redis 缓存服务

    用途：
    - 缓存热门媒体列表
    - 缓存用户会话数据
    - 存储临时计算结果
    """

    def __init__(self, url: str, default_ttl: int):
        self.url = url
        self.default_ttl = default_ttl
        self._client = None

    async def init(self) -> None:
        """
        初始化 Redis 连接

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Redis 初始化")

    async def close(self) -> None:
        """
        关闭 Redis 连接

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Redis 关闭")

    async def get(self, key: str) -> Optional[str]:
        """
        获取缓存值

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Redis get")

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None,
    ) -> None:
        """
        设置缓存值

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Redis set")

    async def delete(self, key: str) -> None:
        """
        删除缓存

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Redis delete")

    async def get_json(self, key: str) -> Optional[Any]:
        """获取 JSON 缓存值"""
        value = await self.get(key)
        if value:
            return json.loads(value)
        return None

    async def set_json(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> None:
        """设置 JSON 缓存值"""
        await self.set(key, json.dumps(value), ttl)

    # ========== 业务方法 ==========

    async def cache_hot_media(self, media_list: list[dict]) -> None:
        """
        缓存热门媒体列表

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现热门媒体缓存")

    async def get_hot_media(self) -> Optional[list[dict]]:
        """
        获取热门媒体列表缓存

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现获取热门媒体缓存")

    async def increment_view_count(self, media_id: int) -> int:
        """
        增加媒体查看次数

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现查看次数增加")


# 全局实例
_redis_service: Optional[RedisService] = None


async def get_redis_service() -> RedisService:
    """获取 Redis 服务实例（依赖注入用）"""
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService(
            url=settings.redis_url,
            default_ttl=settings.redis_cache_ttl,
        )
        await _redis_service.init()
    return _redis_service


async def close_redis_service() -> None:
    """关闭 Redis 服务"""
    global _redis_service
    if _redis_service:
        await _redis_service.close()
        _redis_service = None
