# Backend Services

from .tmdb import TMDBService, get_tmdb_service
from .ai import AIService, get_ai_service
from .scoring import ScoringService, get_scoring_service
from .vector_db import (
    BaseVectorDB,
    create_vector_db,
    get_vector_db,
    close_vector_db,
)
from .redis import RedisService, get_redis_service, close_redis_service
from .supabase import (
    SupabaseService,
    get_supabase_client,
    get_supabase_service,
    close_supabase,
)

__all__ = [
    # TMDB
    "TMDBService",
    "get_tmdb_service",
    # AI
    "AIService",
    "get_ai_service",
    # Scoring
    "ScoringService",
    "get_scoring_service",
    # Vector DB
    "BaseVectorDB",
    "create_vector_db",
    "get_vector_db",
    "close_vector_db",
    # Redis
    "RedisService",
    "get_redis_service",
    "close_redis_service",
    # Supabase
    "SupabaseService",
    "get_supabase_client",
    "get_supabase_service",
    "close_supabase",
]
