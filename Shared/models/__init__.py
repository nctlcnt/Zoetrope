# Shared Models
# 前后端共享的数据模型定义

from .media import MediaType, MediaItem, MediaItemCreate, MediaItemUpdate
from .tmdb import (
    TMDBMediaItem,
    TMDBSearchResponse,
    TMDBMovieDetails,
    TMDBTVDetails,
    TMDBGenre,
    TMDBCredits,
    TMDBCastMember,
)

__all__ = [
    # Media models
    "MediaType",
    "MediaItem",
    "MediaItemCreate",
    "MediaItemUpdate",
    # TMDB models
    "TMDBMediaItem",
    "TMDBSearchResponse",
    "TMDBMovieDetails",
    "TMDBTVDetails",
    "TMDBGenre",
    "TMDBCredits",
    "TMDBCastMember",
]
