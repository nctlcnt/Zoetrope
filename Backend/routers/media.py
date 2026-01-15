# 媒体条目路由
# 提供媒体条目的 CRUD 和查询接口

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database.connection import get_db
from ..models.media import MediaItem, MediaType

router = APIRouter()


# ========== 请求/响应模型 ==========

class MediaCreateRequest(BaseModel):
    """创建媒体条目请求"""
    title: str
    type: str = "movie"  # movie / tv / novel / book / music
    tmdb_id: Optional[int] = None
    release_date: Optional[datetime] = None
    poster_url: Optional[str] = None
    overview: Optional[str] = None


class MediaAddFromTMDBRequest(BaseModel):
    """从 TMDB 搜索结果添加媒体请求"""
    tmdb_id: int = Field(..., description="TMDB ID")
    title: str = Field(..., description="标题（电影）或名称（电视剧）")
    media_type: str = Field(..., description="媒体类型: movie / tv")
    overview: Optional[str] = Field(None, description="简介")
    poster_path: Optional[str] = Field(None, description="海报路径")
    release_date: Optional[str] = Field(None, description="上映日期")
    vote_average: Optional[float] = Field(None, description="TMDB 评分")


class MediaUpdateRequest(BaseModel):
    """更新媒体条目请求"""
    user_score: Optional[float] = None
    is_watched: Optional[int] = None  # 0: 未看, 1: 已看, 2: 在看
    is_hidden: Optional[bool] = None


class MediaResponse(BaseModel):
    """媒体条目响应"""
    id: int
    title: str
    type: str
    tmdb_id: Optional[int]
    release_date: Optional[datetime]
    end_date: Optional[datetime]
    poster_url: Optional[str]
    overview: Optional[str]
    user_score: Optional[float]
    priority_score: float
    mention_count: int
    is_watched: int
    is_hidden: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MediaListResponse(BaseModel):
    """媒体列表响应"""
    items: List[MediaResponse]
    total: int
    page: int
    page_size: int


# ========== 路由端点 ==========

@router.post("/add", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def add_media_from_tmdb(
    request: MediaAddFromTMDBRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    从 TMDB 搜索结果添加媒体到收藏

    如果 TMDB ID 已存在，则更新 mention_count 并返回现有记录
    """
    # 检查是否已存在
    stmt = select(MediaItem).where(MediaItem.tmdb_id == request.tmdb_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # 已存在，增加 mention_count
        existing.mention_count += 1
        existing.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing)
        return existing

    # 解析日期
    release_date = None
    if request.release_date:
        try:
            release_date = datetime.strptime(request.release_date, "%Y-%m-%d")
        except ValueError:
            pass

    # 构建海报 URL
    poster_url = None
    if request.poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{request.poster_path}"

    # 映射媒体类型
    media_type = MediaType.MOVIE if request.media_type == "movie" else MediaType.TV

    # 创建新记录
    new_media = MediaItem(
        title=request.title,
        type=media_type,
        tmdb_id=request.tmdb_id,
        overview=request.overview,
        poster_url=poster_url,
        release_date=release_date,
        priority_score=request.vote_average or 0.0,
        mention_count=1,
    )

    db.add(new_media)
    await db.flush()
    await db.refresh(new_media)

    return new_media

@router.get("/", response_model=MediaListResponse)
async def list_media(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    type: Optional[str] = Query(None, description="媒体类型过滤"),
    sort_by: str = Query("priority", description="排序方式: priority/time/score/mention"),
    is_watched: Optional[int] = Query(None, description="观看状态过滤"),
):
    """
    获取媒体列表

    支持按优先级、时间、评分、提及次数排序

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现媒体列表查询"
    )


@router.get("/carousel")
async def get_carousel_media(
    limit: int = Query(10, ge=1, le=20, description="轮播数量"),
):
    """
    获取轮播推荐媒体

    返回：
    - 最近上映的内容
    - 高热度内容
    - AI 推荐的用户极想看的内容
    - 即将下映提醒

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现轮播推荐"
    )


@router.get("/{media_id}", response_model=MediaResponse)
async def get_media(media_id: int):
    """
    获取单个媒体详情

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现媒体详情查询"
    )


@router.post("/", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def create_media(request: MediaCreateRequest):
    """
    创建媒体条目

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现媒体创建"
    )


@router.patch("/{media_id}", response_model=MediaResponse)
async def update_media(media_id: int, request: MediaUpdateRequest):
    """
    更新媒体条目

    可更新：用户评分、观看状态、隐藏状态

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现媒体更新"
    )


@router.post("/{media_id}/not-interested")
async def mark_not_interested(media_id: int):
    """
    标记"不感兴趣"

    降低该媒体的优先级

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现不感兴趣标记"
    )


@router.post("/{media_id}/watch-later")
async def mark_watch_later(media_id: int):
    """
    标记"稍后再看"

    调整排序优先级

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现稍后再看标记"
    )


@router.delete("/{media_id}")
async def delete_media(media_id: int):
    """
    删除媒体条目

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现媒体删除"
    )
