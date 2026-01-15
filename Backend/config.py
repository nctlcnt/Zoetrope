# 应用配置

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # ========== 服务器配置 ==========
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # CORS 配置
    cors_origins: list[str] = ["*"]

    # ========== TMDB API 配置 ==========
    tmdb_api_key: str = ""
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    tmdb_image_base_url: str = "https://image.tmdb.org/t/p"
    tmdb_default_language: str = "zh-CN"

    # ========== AI 服务配置 ==========
    # OpenAI 兼容 API (支持 OpenAI / Azure / 本地部署)
    ai_api_key: str = ""
    ai_api_base_url: str = "https://api.openai.com/v1"
    ai_model: str = "gpt-4o-mini"
    ai_embedding_model: str = "text-embedding-3-small"

    # ========== 数据库配置 ==========
    # PostgreSQL (可使用 Supabase 提供的连接字符串)
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/zoetrope"

    # ========== Supabase 配置 ==========
    # Supabase 项目 URL 和 API Key
    # 从 Supabase Dashboard -> Settings -> API 获取
    supabase_url: str = ""
    supabase_anon_key: str = ""  # 公开的 anon key
    supabase_service_key: str = ""  # 服务端 service_role key（用于绕过 RLS）

    # ========== Redis 配置 ==========
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_ttl: int = 3600  # 缓存过期时间（秒）

    # ========== 向量数据库配置 ==========
    # 支持: pinecone / weaviate / milvus / chroma
    vector_db_provider: str = "chroma"

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = "zoetrope"

    # Weaviate
    weaviate_url: str = "http://localhost:8080"
    weaviate_api_key: str = ""

    # Milvus
    milvus_host: str = "localhost"
    milvus_port: int = 19530

    # Chroma (本地开发默认)
    chroma_persist_directory: str = "./data/chroma"

    # ========== 评分算法配置 ==========
    # 时间衰减参数
    score_time_decay_factor: float = 0.1
    # 热度权重
    score_hotness_weight: float = 0.3
    # 用户兴趣权重
    score_interest_weight: float = 0.5
    # 时间紧迫性权重
    score_urgency_weight: float = 0.2

    # ========== Inbox 配置 ==========
    inbox_retention_days: int = 7  # 收集箱保留天数

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()
