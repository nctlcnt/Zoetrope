# 评分服务
# 实现优先级评分算法

from datetime import datetime, timedelta
from typing import Optional
from functools import lru_cache

from ..config import settings


class ScoringService:
    """
    评分服务类

    实现 CLAUDE.md 中描述的优先级评分系统：
    - 时间因素（上映/下映紧迫性）
    - 热度因素（被提到次数）
    - 用户兴趣因素（手动评分 + 情感分析）
    - 降权因素（不感兴趣、屏蔽词等）
    """

    def __init__(
        self,
        time_decay_factor: float,
        hotness_weight: float,
        interest_weight: float,
        urgency_weight: float,
    ):
        self.time_decay_factor = time_decay_factor
        self.hotness_weight = hotness_weight
        self.interest_weight = interest_weight
        self.urgency_weight = urgency_weight

    def calculate_priority_score(
        self,
        # 时间因素
        release_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        # 热度因素
        mention_count: int = 0,
        unique_sources: int = 0,
        # 用户兴趣因素
        user_score: Optional[float] = None,
        sentiment_score: Optional[float] = None,
        view_count: int = 0,
        # 降权因素
        not_interested_count: int = 0,
        is_hidden: bool = False,
    ) -> float:
        """
        计算媒体条目的优先级分数

        Args:
            release_date: 上映/发布日期
            end_date: 下映日期
            mention_count: 被提到总次数
            unique_sources: 不同来源数量
            user_score: 用户手动评分 (0-10)
            sentiment_score: AI 情感分析分数 (-1 到 1)
            view_count: 用户查看次数
            not_interested_count: 点击"不感兴趣"次数
            is_hidden: 是否被隐藏

        Returns:
            优先级分数 (0-100)

        TODO: 实现具体的评分算法
        """
        if is_hidden:
            return 0.0

        # TODO: 实现完整的评分算法
        # 以下是占位符逻辑

        score = 50.0  # 基础分

        # 1. 时间紧迫性分数
        urgency_score = self._calculate_urgency_score(release_date, end_date)

        # 2. 热度分数
        hotness_score = self._calculate_hotness_score(mention_count, unique_sources)

        # 3. 用户兴趣分数
        interest_score = self._calculate_interest_score(
            user_score, sentiment_score, view_count
        )

        # 4. 降权处理
        penalty = self._calculate_penalty(not_interested_count)

        # 加权求和
        score = (
            self.urgency_weight * urgency_score
            + self.hotness_weight * hotness_score
            + self.interest_weight * interest_score
            - penalty
        )

        # 归一化到 0-100
        return max(0.0, min(100.0, score))

    def _calculate_urgency_score(
        self,
        release_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> float:
        """
        计算时间紧迫性分数

        - 即将上映：高分
        - 正在上映：中高分
        - 即将下映：极高分
        - 已下映：低分

        TODO: 实现具体逻辑
        """
        return 50.0  # 占位符

    def _calculate_hotness_score(
        self,
        mention_count: int,
        unique_sources: int,
    ) -> float:
        """
        计算热度分数

        - 多个来源提及 > 单一来源多次提及
        - 使用对数衰减避免刷量

        TODO: 实现具体逻辑
        """
        return 50.0  # 占位符

    def _calculate_interest_score(
        self,
        user_score: Optional[float],
        sentiment_score: Optional[float],
        view_count: int,
    ) -> float:
        """
        计算用户兴趣分数

        - 用户评分权重最高
        - 情感分析次之
        - 查看次数作为隐式反馈

        TODO: 实现具体逻辑
        """
        return 50.0  # 占位符

    def _calculate_penalty(self, not_interested_count: int) -> float:
        """
        计算降权惩罚

        TODO: 实现具体逻辑
        """
        return not_interested_count * 10.0  # 占位符


@lru_cache
def get_scoring_service() -> ScoringService:
    """获取评分服务单例（依赖注入用）"""
    return ScoringService(
        time_decay_factor=settings.score_time_decay_factor,
        hotness_weight=settings.score_hotness_weight,
        interest_weight=settings.score_interest_weight,
        urgency_weight=settings.score_urgency_weight,
    )
