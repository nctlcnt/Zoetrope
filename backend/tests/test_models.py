"""Tests for media models"""

import pytest
from datetime import datetime
from app.models import MediaItem, MediaType, PriorityLevel, MediaStatus


def test_media_item_creation():
    """Test creating a media item"""
    media = MediaItem(
        title="Test Movie",
        media_type=MediaType.MOVIE,
        priority=PriorityLevel.HIGH,
        status=MediaStatus.WANT_TO_WATCH
    )
    
    assert media.title == "Test Movie"
    assert media.media_type == MediaType.MOVIE
    assert media.priority == PriorityLevel.HIGH
    assert media.status == MediaStatus.WANT_TO_WATCH
    assert media.appearance_count == 1


def test_media_type_enum():
    """Test media type enum values"""
    assert MediaType.MOVIE.value == "movie"
    assert MediaType.TV_SHOW.value == "tv_show"
    assert MediaType.NOVEL.value == "novel"
    assert MediaType.BOOK.value == "book"


def test_priority_level_enum():
    """Test priority level enum values"""
    assert PriorityLevel.HIGH.value == "high"
    assert PriorityLevel.MEDIUM.value == "medium"
    assert PriorityLevel.LOW.value == "low"
