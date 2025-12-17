"""Database models for Zoetrope"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class MediaType(enum.Enum):
    """Media types supported by the app"""
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    NOVEL = "novel"
    BOOK = "book"


class PriorityLevel(enum.Enum):
    """Priority levels for media items"""
    HIGH = "high"  # 急切想看
    MEDIUM = "medium"
    LOW = "low"  # 剧荒备选


class MediaStatus(enum.Enum):
    """Viewing status of media"""
    WANT_TO_WATCH = "want_to_watch"
    WATCHING = "watching"
    WATCHED = "watched"
    DROPPED = "dropped"


class MediaItem(Base):
    """Main media item model"""
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    media_type = Column(Enum(MediaType), nullable=False)
    status = Column(Enum(MediaStatus), default=MediaStatus.WANT_TO_WATCH)
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.MEDIUM)
    
    # User input
    reason_to_watch = Column(Text)  # 想看的原因
    trailer_url = Column(String(500))  # 预告片链接
    recommendation_text = Column(Text)  # 推荐文案
    
    # External data
    release_date = Column(DateTime)  # 上映时间
    end_date = Column(DateTime)  # 下映时间
    tmdb_id = Column(String(50), index=True)  # TMDB ID
    imdb_id = Column(String(50), index=True)  # IMDB ID
    poster_url = Column(String(500))
    rating = Column(Float)
    
    # AI generated
    ai_summary = Column(Text)  # AI总结的吸引点
    ai_motivation = Column(Text)  # AI提取的观看动机
    
    # Metadata
    appearance_count = Column(Integer, default=1)  # 出现在榜单的次数
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_reminded_at = Column(DateTime)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="media_item", cascade="all, delete-orphan")
    streaming_links = relationship("StreamingLink", back_populates="media_item", cascade="all, delete-orphan")


class Recommendation(Base):
    """Recommendations from different sources/bloggers"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    media_item_id = Column(Integer, ForeignKey("media_items.id"), nullable=False)
    
    source_name = Column(String(255))  # 博主/公众号名称
    source_url = Column(String(500))
    recommendation_reason = Column(Text)  # 推荐理由
    rating = Column(Float)
    review_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    media_item = relationship("MediaItem", back_populates="recommendations")


class StreamingLink(Base):
    """Links to streaming platforms"""
    __tablename__ = "streaming_links"

    id = Column(Integer, primary_key=True, index=True)
    media_item_id = Column(Integer, ForeignKey("media_items.id"), nullable=False)
    
    platform = Column(String(100))  # Netflix, Disney+, etc.
    url = Column(String(500))
    available = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    media_item = relationship("MediaItem", back_populates="streaming_links")


class UserSettings(Base):
    """User preferences and settings"""
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    
    # Notification preferences
    enable_reminders = Column(Boolean, default=True)
    reminder_days_before = Column(Integer, default=3)  # 提前几天提醒
    
    # Preferred platforms
    preferred_platforms = Column(Text)  # JSON array of platforms
    
    # AI settings
    ai_enabled = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
