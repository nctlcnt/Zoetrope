# 评论模型
# TODO: 实现完整的 ORM 模型

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..database.connection import Base


class CommentSource(str, Enum):
    """评论来源"""
    USER = "user"  # 用户手动添加
    AI = "ai"  # AI 生成
    IMPORTED = "imported"  # 从博文/榜单导入


class Comment(Base):
    """
    评论表

    对应 CLAUDE.md 中的 Comment 数据模型
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 关联媒体
    media_id = Column(Integer, ForeignKey("media_items.id"), nullable=False, index=True)

    # 评论内容
    content = Column(Text, nullable=False)

    # 来源信息
    source = Column(SQLEnum(CommentSource), default=CommentSource.USER)
    source_url = Column(String(500), nullable=True)  # 原始来源 URL
    source_author = Column(String(100), nullable=True)  # 原作者/博主

    # AI 分析结果
    sentiment_score = Column(Float, nullable=True)  # 情感分数 (-1 到 1)
    extracted_rating = Column(Float, nullable=True)  # 从评论中提取的评分

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联关系
    # media = relationship("MediaItem", back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, media_id={self.media_id}, source={self.source})>"
