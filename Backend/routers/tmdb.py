# TMDB API 路由
# 提供 TMDB 数据的代理和封装

from typing import Optional
from fastapi import APIRouter, Depends, Query

from ..services.tmdb import TMDBService, get_tmdb_service

import sys
sys.path.insert(0, str(__file__).rsplit("/Backend", 1)[0])
from Shared.models.tmdb import (
    TMDBSearchResponse,
    TMDBMovieDetails,
    TMDBTVDetails,
)

router = APIRouter()


@router.get("/search/movie", response_model=TMDBSearchResponse)
async def search_movies(
    query: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码，如 zh-CN"),
    year: Optional[int] = Query(None, description="上映年份"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    搜索电影

    - **query**: 搜索关键词
    - **page**: 页码，从1开始
    - **language**: 语言代码，默认 zh-CN
    - **year**: 过滤特定年份的电影
    """
    return await tmdb.search_movies(
        query=query,
        page=page,
        language=language,
        year=year,
    )


@router.get("/search/tv", response_model=TMDBSearchResponse)
async def search_tv_shows(
    query: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码"),
    first_air_date_year: Optional[int] = Query(None, description="首播年份"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    搜索电视剧

    - **query**: 搜索关键词
    - **page**: 页码，从1开始
    - **language**: 语言代码，默认 zh-CN
    - **first_air_date_year**: 过滤特定首播年份的电视剧
    """
    return await tmdb.search_tv_shows(
        query=query,
        page=page,
        language=language,
        first_air_date_year=first_air_date_year,
    )


@router.get("/search/multi", response_model=TMDBSearchResponse)
async def search_multi(
    query: str = Query(..., description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    综合搜索（电影+电视剧）

    - **query**: 搜索关键词
    - **page**: 页码，从1开始
    - **language**: 语言代码，默认 zh-CN
    """
    return await tmdb.search_multi(
        query=query,
        page=page,
        language=language,
    )


@router.get("/movie/{movie_id}", response_model=TMDBMovieDetails)
async def get_movie_details(
    movie_id: int,
    language: Optional[str] = Query(None, description="语言代码"),
    append_to_response: Optional[str] = Query(
        None, description="附加信息，如 credits,videos"
    ),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBMovieDetails:
    """
    获取电影详情

    - **movie_id**: TMDB 电影 ID
    - **language**: 语言代码，默认 zh-CN
    - **append_to_response**: 附加信息，逗号分隔
    """
    return await tmdb.get_movie_details(
        movie_id=movie_id,
        language=language,
        append_to_response=append_to_response,
    )


@router.get("/tv/{tv_id}", response_model=TMDBTVDetails)
async def get_tv_details(
    tv_id: int,
    language: Optional[str] = Query(None, description="语言代码"),
    append_to_response: Optional[str] = Query(
        None, description="附加信息，如 credits,videos"
    ),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBTVDetails:
    """
    获取电视剧详情

    - **tv_id**: TMDB 电视剧 ID
    - **language**: 语言代码，默认 zh-CN
    - **append_to_response**: 附加信息，逗号分隔
    """
    return await tmdb.get_tv_details(
        tv_id=tv_id,
        language=language,
        append_to_response=append_to_response,
    )


@router.get("/movie/{movie_id}/now_playing")
async def get_now_playing_movies(
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码"),
    region: Optional[str] = Query(None, description="地区代码，如 CN"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    获取正在上映的电影

    - **page**: 页码，从1开始
    - **language**: 语言代码，默认 zh-CN
    - **region**: 地区代码，如 CN 表示中国大陆
    """
    return await tmdb.get_now_playing_movies(
        page=page,
        language=language,
        region=region,
    )


@router.get("/movie/{movie_id}/upcoming")
async def get_upcoming_movies(
    page: int = Query(1, ge=1, description="页码"),
    language: Optional[str] = Query(None, description="语言代码"),
    region: Optional[str] = Query(None, description="地区代码，如 CN"),
    tmdb: TMDBService = Depends(get_tmdb_service),
) -> TMDBSearchResponse:
    """
    获取即将上映的电影

    - **page**: 页码，从1开始
    - **language**: 语言代码，默认 zh-CN
    - **region**: 地区代码，如 CN 表示中国大陆
    """
    return await tmdb.get_upcoming_movies(
        page=page,
        language=language,
        region=region,
    )
