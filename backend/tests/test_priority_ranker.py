"""Tests for priority ranker"""

import pytest
from datetime import datetime, timedelta
from app.priority_ranker import PriorityRanker
from app.models import MediaItem, MediaType, PriorityLevel, MediaStatus


def test_priority_score_calculation():
    """Test priority score calculation"""
    ranker = PriorityRanker()
    
    # Create a high priority item
    item = MediaItem(
        title="Test",
        media_type=MediaType.MOVIE,
        priority=PriorityLevel.HIGH,
        appearance_count=3,
        created_at=datetime.utcnow(),
        rating=8.5
    )
    
    score = ranker.calculate_priority_score(item)
    assert score > 0
    
    # High priority should have higher score than low priority
    low_item = MediaItem(
        title="Test2",
        media_type=MediaType.MOVIE,
        priority=PriorityLevel.LOW,
        appearance_count=1,
        created_at=datetime.utcnow(),
        rating=5.0
    )
    
    low_score = ranker.calculate_priority_score(low_item)
    assert score > low_score


def test_auto_adjust_priority():
    """Test automatic priority adjustment"""
    ranker = PriorityRanker()
    
    # Item with 3+ appearances should be upgraded to high
    item = MediaItem(
        title="Test",
        media_type=MediaType.MOVIE,
        priority=PriorityLevel.MEDIUM,
        appearance_count=3
    )
    
    new_priority = ranker.auto_adjust_priority(item)
    assert new_priority == "high"
    
    # Item with 2 appearances and low priority should be upgraded to medium
    item2 = MediaItem(
        title="Test2",
        media_type=MediaType.MOVIE,
        priority=PriorityLevel.LOW,
        appearance_count=2
    )
    
    new_priority2 = ranker.auto_adjust_priority(item2)
    assert new_priority2 == "medium"
