"""Pydantic schemas for API request/response"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MediaTypeEnum(str, Enum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    NOVEL = "novel"
    BOOK = "book"


class PriorityLevelEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MediaStatusEnum(str, Enum):
    WANT_TO_WATCH = "want_to_watch"
    WATCHING = "watching"
    WATCHED = "watched"
    DROPPED = "dropped"


class MediaItemCreate(BaseModel):
    """Schema for creating a media item"""
    title: str = Field(..., min_length=1, max_length=255)
    media_type: MediaTypeEnum
    reason_to_watch: Optional[str] = None
    trailer_url: Optional[str] = None
    recommendation_text: Optional[str] = None
    priority: PriorityLevelEnum = PriorityLevelEnum.MEDIUM


class MediaItemUpdate(BaseModel):
    """Schema for updating a media item"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[MediaStatusEnum] = None
    priority: Optional[PriorityLevelEnum] = None
    reason_to_watch: Optional[str] = None
    trailer_url: Optional[str] = None
    recommendation_text: Optional[str] = None


class RecommendationBase(BaseModel):
    """Base schema for recommendations"""
    source_name: str
    source_url: Optional[str] = None
    recommendation_reason: Optional[str] = None
    rating: Optional[float] = None


class RecommendationResponse(RecommendationBase):
    """Schema for recommendation response"""
    id: int
    review_date: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StreamingLinkBase(BaseModel):
    """Base schema for streaming links"""
    platform: str
    url: str
    available: bool = True


class StreamingLinkResponse(StreamingLinkBase):
    """Schema for streaming link response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MediaItemResponse(BaseModel):
    """Schema for media item response"""
    id: int
    title: str
    media_type: str
    status: str
    priority: str
    reason_to_watch: Optional[str] = None
    trailer_url: Optional[str] = None
    recommendation_text: Optional[str] = None
    release_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    poster_url: Optional[str] = None
    rating: Optional[float] = None
    ai_summary: Optional[str] = None
    ai_motivation: Optional[str] = None
    appearance_count: int
    created_at: datetime
    updated_at: datetime
    recommendations: List[RecommendationResponse] = []
    streaming_links: List[StreamingLinkResponse] = []

    class Config:
        from_attributes = True


class CarouselResponse(BaseModel):
    """Schema for carousel data"""
    title: str
    items: List[MediaItemResponse]


class DashboardResponse(BaseModel):
    """Schema for dashboard with multiple carousels"""
    latest_wants: CarouselResponse
    ending_soon: CarouselResponse
    recently_released: CarouselResponse
