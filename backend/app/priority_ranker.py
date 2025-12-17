"""Priority ranking service using machine learning"""

from typing import List
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import numpy as np


class PriorityRanker:
    """Service for dynamically ranking media items by priority"""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def calculate_priority_score(self, media_item) -> float:
        """
        Calculate priority score based on multiple factors:
        - User-set priority (high/medium/low)
        - Appearance count (how many times it appeared in lists)
        - Recency of addition
        - Release date proximity
        - AI analysis quality
        """
        score = 0.0
        
        # Base priority weight (0-100)
        priority_weights = {
            "high": 100,
            "medium": 50,
            "low": 25
        }
        score += priority_weights.get(media_item.priority.value, 50)
        
        # Appearance count bonus (more appearances = higher priority)
        # Multiple appearances in different lists should boost priority
        appearance_bonus = min(media_item.appearance_count * 10, 50)
        score += appearance_bonus
        
        # Recency bonus (recently added items get slight boost)
        if media_item.created_at:
            days_old = (datetime.utcnow() - media_item.created_at).days
            recency_bonus = max(20 - days_old, 0)
            score += recency_bonus
        
        # Release date proximity (items releasing soon get boost)
        if media_item.release_date:
            days_until_release = (media_item.release_date - datetime.utcnow()).days
            if -7 <= days_until_release <= 30:  # Released in last week or releasing in next month
                proximity_bonus = 30 - abs(days_until_release)
                score += max(proximity_bonus, 0)
        
        # End date urgency (items ending soon get high boost)
        if media_item.end_date:
            days_until_end = (media_item.end_date - datetime.utcnow()).days
            if 0 <= days_until_end <= 14:  # Ending in next 2 weeks
                urgency_bonus = 50 * (1 - days_until_end / 14)
                score += urgency_bonus
        
        # AI analysis quality bonus
        if media_item.ai_summary and media_item.ai_motivation:
            score += 10
        
        # Rating bonus
        if media_item.rating:
            score += media_item.rating * 2  # 0-20 points based on 0-10 rating
        
        return score
    
    def rank_items(self, items: List) -> List:
        """Rank media items by calculated priority score"""
        if not items:
            return []
        
        # Calculate scores for all items
        scored_items = []
        for item in items:
            score = self.calculate_priority_score(item)
            scored_items.append((item, score))
        
        # Sort by score (descending)
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        return [item for item, score in scored_items]
    
    def auto_adjust_priority(self, media_item) -> str:
        """
        Automatically adjust priority based on appearance count
        If item appears in multiple lists (3+), upgrade to high priority
        """
        if media_item.appearance_count >= 3 and media_item.priority.value != "high":
            return "high"
        elif media_item.appearance_count >= 2 and media_item.priority.value == "low":
            return "medium"
        
        return media_item.priority.value
