# Media 数据模型
# 与前端 MediaItem.swift 保持一致

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MediaType(str, Enum):
    """媒体类型枚举"""
    movie = "movie"
    tv_show = "tvShow"
    novel = "novel"
    book = "book"
    music = "music"


class MediaItemBase(BaseModel):
    """媒体条目基础字段"""
    title: str = Field(..., description="媒体标题")
    type: MediaType = Field(..., description="媒体类型")
    release_date: Optional[datetime] = Field(None, description="上映/发布日期")
    end_date: Optional[datetime] = Field(None, description="下映日期")
    poster_url: Optional[str] = Field(None, description="海报图片URL")
    summary: Optional[str] = Field(None, description="AI生成或用户添加的简介")

    # TMDB 关联
    tmdb_id: Optional[int] = Field(None, description="TMDB ID")


class MediaItemCreate(MediaItemBase):
    """创建媒体条目的请求模型"""
    user_score: Optional[float] = Field(None, ge=0, le=10, description="用户评分 0-10")


class MediaItemUpdate(BaseModel):
    """更新媒体条目的请求模型"""
    title: Optional[str] = None
    summary: Optional[str] = None
    release_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    poster_url: Optional[str] = None
    user_score: Optional[float] = Field(None, ge=0, le=10)
    is_watched: Optional[bool] = None
    is_not_interested: Optional[bool] = None


class MediaItem(MediaItemBase):
    """完整的媒体条目模型"""
    id: UUID = Field(..., description="唯一标识符")

    # 评分与优先级
    user_score: Optional[float] = Field(None, ge=0, le=10, description="用户评分")
    priority_score: float = Field(default=0.0, description="系统计算的优先级分数")
    mention_count: int = Field(default=0, description="被提及次数")

    # 时间戳与状态
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    is_watched: bool = Field(default=False, description="是否已观看")
    is_not_interested: bool = Field(default=False, description="是否标记为不感兴趣")

    class Config:
        from_attributes = True
