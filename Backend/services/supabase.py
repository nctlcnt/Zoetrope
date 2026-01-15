# Supabase 服务
# 提供 Supabase 客户端的初始化和常用操作

from typing import Optional
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

from ..config import settings


# Supabase 客户端单例
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    获取 Supabase 客户端单例

    使用 service_role key 以绕过 RLS (Row Level Security)
    适用于后端服务

    Returns:
        Supabase Client 实例
    """
    global _supabase_client

    if _supabase_client is None:
        if not settings.supabase_url or not settings.supabase_service_key:
            raise RuntimeError(
                "Supabase configuration missing. "
                "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env"
            )

        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_service_key,
            options=ClientOptions(
                auto_refresh_token=False,
                persist_session=False,
            )
        )

    return _supabase_client


def get_supabase_anon_client() -> Client:
    """
    获取使用 anon key 的 Supabase 客户端

    遵循 RLS 规则，适用于需要权限控制的场景

    Returns:
        Supabase Client 实例
    """
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise RuntimeError(
            "Supabase configuration missing. "
            "Please set SUPABASE_URL and SUPABASE_ANON_KEY in .env"
        )

    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key,
    )


async def close_supabase() -> None:
    """关闭 Supabase 客户端连接"""
    global _supabase_client
    # Supabase Python 客户端目前不需要显式关闭
    _supabase_client = None


class SupabaseService:
    """
    Supabase 服务封装

    提供常用的数据库操作方法
    """

    def __init__(self, client: Optional[Client] = None):
        self.client = client or get_supabase_client()

    # ========== 媒体相关操作 ==========

    async def get_media_by_tmdb_id(self, tmdb_id: int) -> Optional[dict]:
        """根据 TMDB ID 查询媒体"""
        response = self.client.table("media_items").select("*").eq("tmdb_id", tmdb_id).execute()
        return response.data[0] if response.data else None

    async def create_media(self, data: dict) -> dict:
        """创建媒体记录"""
        response = self.client.table("media_items").insert(data).execute()
        return response.data[0]

    async def update_media(self, media_id: int, data: dict) -> dict:
        """更新媒体记录"""
        response = self.client.table("media_items").update(data).eq("id", media_id).execute()
        return response.data[0]

    async def list_media(
        self,
        page: int = 1,
        page_size: int = 20,
        order_by: str = "priority_score",
        ascending: bool = False,
    ) -> tuple[list[dict], int]:
        """
        获取媒体列表

        Returns:
            (items, total_count)
        """
        offset = (page - 1) * page_size

        # 获取总数
        count_response = self.client.table("media_items").select("*", count="exact").execute()
        total = count_response.count or 0

        # 获取分页数据
        response = (
            self.client.table("media_items")
            .select("*")
            .order(order_by, desc=not ascending)
            .range(offset, offset + page_size - 1)
            .execute()
        )

        return response.data, total

    # ========== 评论相关操作 ==========

    async def get_comments_by_media_id(self, media_id: int) -> list[dict]:
        """获取媒体的所有评论"""
        response = (
            self.client.table("comments")
            .select("*")
            .eq("media_id", media_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    async def create_comment(self, data: dict) -> dict:
        """创建评论"""
        response = self.client.table("comments").insert(data).execute()
        return response.data[0]

    # ========== Inbox 相关操作 ==========

    async def create_inbox_item(self, data: dict) -> dict:
        """创建收集箱条目"""
        response = self.client.table("inbox").insert(data).execute()
        return response.data[0]

    async def get_pending_inbox_items(self) -> list[dict]:
        """获取待处理的收集箱条目"""
        response = (
            self.client.table("inbox")
            .select("*")
            .eq("processed", False)
            .execute()
        )
        return response.data


# 依赖注入
def get_supabase_service() -> SupabaseService:
    """FastAPI 依赖注入用"""
    return SupabaseService()
