# FastAPI 应用入口

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import register_routers
from .database import init_db, close_db
from .services import close_vector_db, close_redis_service, close_supabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()

    yield

    # 关闭时清理资源
    await close_db()
    await close_supabase()
    await close_vector_db()
    await close_redis_service()


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    app = FastAPI(
        title="Zoetrope API",
        description="媒体收藏推荐服务后端",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS 配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    register_routers(app)

    @app.get("/health")
    async def health_check():
        """健康检查端点"""
        return {"status": "ok"}

    return app


# 默认应用实例
app = create_app()
