# Backend Routers
# 集中管理所有 API 路由

from fastapi import APIRouter, FastAPI

from .tmdb import router as tmdb_router
from .media import router as media_router
from .inbox import router as inbox_router
from .comment import router as comment_router
from .search import router as search_router

# 路由配置表
ROUTER_CONFIG = [
    {"router": search_router, "prefix": "/api/search", "tags": ["Search"]},
    {"router": tmdb_router, "prefix": "/api/tmdb", "tags": ["TMDB"]},
    {"router": media_router, "prefix": "/api/media", "tags": ["Media"]},
    {"router": inbox_router, "prefix": "/api/inbox", "tags": ["Inbox"]},
    {"router": comment_router, "prefix": "/api/comments", "tags": ["Comments"]},
]


def register_routers(app: FastAPI) -> None:
    """
    注册所有路由到 FastAPI 应用

    Args:
        app: FastAPI 应用实例
    """
    for config in ROUTER_CONFIG:
        app.include_router(
            config["router"],
            prefix=config["prefix"],
            tags=config["tags"],
        )


__all__ = [
    "register_routers",
    "ROUTER_CONFIG",
    "search_router",
    "tmdb_router",
    "media_router",
    "inbox_router",
    "comment_router",
]
