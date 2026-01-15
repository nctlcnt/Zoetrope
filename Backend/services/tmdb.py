# TMDB API 服务
# 封装 TMDB API 调用

from typing import Any, Optional
import httpx
from functools import lru_cache

from ..config import settings

import sys
sys.path.insert(0, str(__file__).rsplit("/Backend", 1)[0])
from Shared.models.tmdb import (
    TMDBSearchResponse,
    TMDBMovieDetails,
    TMDBTVDetails,
)


class TMDBServiceError(Exception):
    """TMDB 服务错误"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TMDBService:
    """TMDB API 服务类"""

    def __init__(self, api_key: str, base_url: str, default_language: str = "zh-CN"):
        self.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYzFiYzRkNTBmZGQ0ZTJkZTRlNGE2MTVlMWViZDUwYiIsIm5iZiI6MTYzMDI0MTA4My4xMzQsInN1YiI6IjYxMmI4MTNiMjIzZTIwMDA5MTNjNTI2NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XvVDawikrAxIUl7Blv0TFRWYsQqiY0VoGhiJjjkC1ow"
        self.base_url = base_url.rstrip("/")
        self.default_language = default_language
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建 HTTP 客户端"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Accept": "application/json",
                },
            )
        return self._client

    async def close(self):
        """关闭 HTTP 客户端"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        发送 API 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            params: 查询参数

        Returns:
            响应数据

        Raises:
            TMDBServiceError: API 请求失败
        """
        client = await self._get_client()

        # 添加默认语言参数
        if params is None:
            params = {}
        if "language" not in params or params["language"] is None:
            params["language"] = self.default_language

        # 移除 None 值
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = await client.request(method, endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise TMDBServiceError(
                f"TMDB API error: {e.response.text}",
                status_code=e.response.status_code,
            )
        except httpx.RequestError as e:
            raise TMDBServiceError(f"Request failed: {str(e)}")

    # ========== 搜索 API ==========

    async def search_movies(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
        year: Optional[int] = None,
    ) -> TMDBSearchResponse:
        """
        搜索电影

        Args:
            query: 搜索关键词
            page: 页码
            language: 语言代码
            year: 上映年份

        Returns:
            搜索结果
        """
        data = await self._request(
            "GET",
            "/search/movie",
            params={
                "query": query,
                "page": page,
                "language": language,
                "year": year,
            },
        )
        return TMDBSearchResponse(**data)

    async def search_tv_shows(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
        first_air_date_year: Optional[int] = None,
    ) -> TMDBSearchResponse:
        """
        搜索电视剧

        Args:
            query: 搜索关键词
            page: 页码
            language: 语言代码
            first_air_date_year: 首播年份

        Returns:
            搜索结果
        """
        data = await self._request(
            "GET",
            "/search/tv",
            params={
                "query": query,
                "page": page,
                "language": language,
                "first_air_date_year": first_air_date_year,
            },
        )
        return TMDBSearchResponse(**data)

    async def search_multi(
        self,
        query: str,
        page: int = 1,
        language: Optional[str] = None,
    ) -> TMDBSearchResponse:
        """
        综合搜索（电影+电视剧）

        Args:
            query: 搜索关键词
            page: 页码
            language: 语言代码

        Returns:
            搜索结果
        """
        data = await self._request(
            "GET",
            "/search/multi",
            params={
                "query": query,
                "page": page,
                "language": language,
            },
        )
        return TMDBSearchResponse(**data)

    # ========== 详情 API ==========

    async def get_movie_details(
        self,
        movie_id: int,
        language: Optional[str] = None,
        append_to_response: Optional[str] = None,
    ) -> TMDBMovieDetails:
        """
        获取电影详情

        Args:
            movie_id: TMDB 电影 ID
            language: 语言代码
            append_to_response: 附加信息，如 "credits,videos"

        Returns:
            电影详情
        """
        data = await self._request(
            "GET",
            f"/movie/{movie_id}",
            params={
                "language": language,
                "append_to_response": append_to_response,
            },
        )
        return TMDBMovieDetails(**data)

    async def get_tv_details(
        self,
        tv_id: int,
        language: Optional[str] = None,
        append_to_response: Optional[str] = None,
    ) -> TMDBTVDetails:
        """
        获取电视剧详情

        Args:
            tv_id: TMDB 电视剧 ID
            language: 语言代码
            append_to_response: 附加信息，如 "credits,videos"

        Returns:
            电视剧详情
        """
        data = await self._request(
            "GET",
            f"/tv/{tv_id}",
            params={
                "language": language,
                "append_to_response": append_to_response,
            },
        )
        return TMDBTVDetails(**data)

    # ========== 列表 API ==========

    async def get_now_playing_movies(
        self,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
    ) -> TMDBSearchResponse:
        """
        获取正在上映的电影

        Args:
            page: 页码
            language: 语言代码
            region: 地区代码，如 "CN"

        Returns:
            电影列表
        """
        data = await self._request(
            "GET",
            "/movie/now_playing",
            params={
                "page": page,
                "language": language,
                "region": region,
            },
        )
        return TMDBSearchResponse(**data)

    async def get_upcoming_movies(
        self,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
    ) -> TMDBSearchResponse:
        """
        获取即将上映的电影

        Args:
            page: 页码
            language: 语言代码
            region: 地区代码，如 "CN"

        Returns:
            电影列表
        """
        data = await self._request(
            "GET",
            "/movie/upcoming",
            params={
                "page": page,
                "language": language,
                "region": region,
            },
        )
        return TMDBSearchResponse(**data)

    async def get_popular_movies(
        self,
        page: int = 1,
        language: Optional[str] = None,
        region: Optional[str] = None,
    ) -> TMDBSearchResponse:
        """
        获取热门电影

        Args:
            page: 页码
            language: 语言代码
            region: 地区代码

        Returns:
            电影列表
        """
        data = await self._request(
            "GET",
            "/movie/popular",
            params={
                "page": page,
                "language": language,
                "region": region,
            },
        )
        return TMDBSearchResponse(**data)

    async def get_popular_tv_shows(
        self,
        page: int = 1,
        language: Optional[str] = None,
    ) -> TMDBSearchResponse:
        """
        获取热门电视剧

        Args:
            page: 页码
            language: 语言代码

        Returns:
            电视剧列表
        """
        data = await self._request(
            "GET",
            "/tv/popular",
            params={
                "page": page,
                "language": language,
            },
        )
        return TMDBSearchResponse(**data)


@lru_cache
def get_tmdb_service() -> TMDBService:
    """获取 TMDB 服务单例（依赖注入用）"""
    return TMDBService(
        api_key=settings.tmdb_api_key,
        base_url=settings.tmdb_base_url,
        default_language=settings.tmdb_default_language,
    )
