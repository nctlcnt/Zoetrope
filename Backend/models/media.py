# 媒体条目模型
# TODO: 实现完整的 ORM 模型

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from ..database.connection import Base


class MediaType(str, Enum):
    """媒体类型"""
    MOVIE = "movie"
    TV = "tv"
    NOVEL = "novel"
    BOOK = "book"
    MUSIC = "music"


class MediaItem(Base):
    """
    媒体条目表

    对应 CLAUDE.md 中的 Media Item 数据模型
    """
    __tablename__ = "media_items"

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    type = Column(SQLEnum(MediaType), nullable=False, default=MediaType.MOVIE)

    # 外部数据源 ID
    tmdb_id = Column(Integer, nullable=True, unique=True, index=True)
    imdb_id = Column(String(20), nullable=True, unique=True)

    # 时间信息
    release_date = Column(DateTime, nullable=True)  # 上映/发布日期
    end_date = Column(DateTime, nullable=True)  # 下映日期（电影）/ 完结日期（剧集）

    # 媒体信息
    poster_url = Column(String(500), nullable=True)
    overview = Column(Text, nullable=True)  # 简介

    # 评分相关
    user_score = Column(Float, nullable=True)  # 用户手动评分 (0-10)
    priority_score = Column(Float, default=0.0)  # 系统计算的优先级分数
    sentiment_score = Column(Float, nullable=True)  # AI 分析的情感分数

    # 统计数据
    mention_count = Column(Integer, default=0)  # 被提到次数
    view_count = Column(Integer, default=0)  # 用户查看次数

    # 状态标记
    is_watched = Column(Integer, default=0)  # 是否已观看 (0: 未看, 1: 已看, 2: 在看)
    is_hidden = Column(Integer, default=0)  # 是否隐藏（不再提醒）

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    # comments = relationship("Comment", back_populates="media", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<MediaItem(id={self.id}, title='{self.title}', type={self.type})>"
