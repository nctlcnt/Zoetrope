# 数据库连接管理
# 支持本地 PostgreSQL 和 Supabase

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from ..config import settings

# SQLAlchemy Base
Base = declarative_base()

# 异步引擎（延迟初始化）
_engine = None
_async_session_maker = None


async def init_db() -> None:
    """
    初始化数据库连接

    支持本地 PostgreSQL 和 Supabase 连接
    Supabase 使用 connection pooling，建议使用 NullPool
    """
    global _engine, _async_session_maker

    # 检测是否为 Supabase 连接（通过 URL 判断）
    is_supabase = "supabase" in settings.database_url.lower()

    # Supabase 连接池配置
    # Supabase 使用 PgBouncer，建议使用 NullPool 或设置 prepared_statement_cache_size=0
    engine_kwargs = {
        "echo": settings.debug,
        "pool_pre_ping": True,
    }

    if is_supabase:
        # Supabase 使用 transaction mode pooling
        # 禁用 SQLAlchemy 连接池，让 Supabase 处理
        engine_kwargs["poolclass"] = NullPool
        # 禁用 prepared statements（Supabase transaction mode 不支持）
        engine_kwargs["connect_args"] = {
            "prepared_statement_cache_size": 0,
        }

    _engine = create_async_engine(
        settings.database_url,
        **engine_kwargs,
    )

    _async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # 创建所有表（如果不存在）
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """关闭数据库连接"""
    global _engine
    if _engine:
        await _engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话（依赖注入用）

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    if _async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with _async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
