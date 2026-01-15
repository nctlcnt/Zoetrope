# 统一搜索路由
# 处理所有前端发来的搜索请求，根据 scope 参数路由到不同的搜索服务

from enum import Enum
from typing import Optional, Union
from fastapi import APIRouter, Depends, Query, HTTPException

from ..services.tmdb import TMDBService, get_tmdb_service

import sys
sys.path.insert(0, str(__file__).rsplit("/Backend", 1)[0])
from Shared.models.tmdb import TMDBSearchResponse


class SearchScope(str, Enum):
    """搜索范围枚举"""
    TMDB = "tmdb"           # TMDB 综合搜索
    TMDB_MOVIE = "tmdb_movie"   # TMDB 电影搜索
    TMDB_TV = "tmdb_tv"     # TMDB 电视剧搜索
    MEDIA = "media"         # 本地媒体库搜索（待实现）


router = APIRouter()


@router.get("", response_model=TMDBSearchResponse)
async def unified_search(
    query: str = Query(..., min_length=1, description="搜索关键词"),
    scope: SearchScope = Query(SearchScope.TMDB, description="搜索范围"),
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码，如 zh-CN"),
    year: Optional[int] = Query(None, description="年份过滤"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    统一搜索接口

    根据 scope 参数路由到不同的搜索服务：
    - **tmdb**: TMDB 综合搜索（电影+电视剧）
    - **tmdb_movie**: 仅搜索 TMDB 电影
    - **tmdb_tv**: 仅搜索 TMDB 电视剧
    - **media**: 搜索本地媒体库（待实现）

    示例请求：
    - `/api/search?scope=tmdb&query=盗梦空间`
    - `/api/search?scope=tmdb_movie&query=星际穿越&year=2014`
    """
    match scope:
        case SearchScope.TMDB:
            return await tmdb.search_multi(
                query=query,
                page=page,
                language=language,
            )

        case SearchScope.TMDB_MOVIE:
            return await tmdb.search_movies(
                query=query,
                page=page,
                language=language,
                year=year,
            )

        case SearchScope.TMDB_TV:
            return await tmdb.search_tv_shows(
                query=query,
                page=page,
                language=language,
                first_air_date_year=year,
            )

        case SearchScope.MEDIA:
            # TODO: 实现本地媒体库搜索
            raise HTTPException(
                status_code=501,
                detail="本地媒体库搜索功能尚未实现"
            )


@router.get("/scopes")
async def get_available_scopes() -> dict:
    """
    获取可用的搜索范围列表

    返回所有支持的 scope 参数及其描述
    """
    return {
        "scopes": [
            {
                "value": SearchScope.TMDB.value,
                "label": "TMDB 综合搜索",
                "description": "同时搜索电影和电视剧",
            },
            {
                "value": SearchScope.TMDB_MOVIE.value,
                "label": "TMDB 电影",
                "description": "仅搜索电影",
            },
            {
                "value": SearchScope.TMDB_TV.value,
                "label": "TMDB 电视剧",
                "description": "仅搜索电视剧",
            },
            {
                "value": SearchScope.MEDIA.value,
                "label": "我的收藏",
                "description": "搜索已添加的媒体（待实现）",
            },
        ]
    }
