# 收集箱模型
# TODO: 实现完整的 ORM 模型

from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql.elements import ColumnElement

from ..database.connection import Base
from ..config import settings


class InboxItem(Base):
    """
    收集箱表

    对应 CLAUDE.md 中的 Inbox 数据模型
    暂存用户粘贴的原始内容，定期自动清理
    """
    __tablename__ = "inbox_items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 原始内容
    raw_content = Column(Text, nullable=False)
    url = Column(String(500), nullable=True)  # 可选的原始 URL

    # 处理状态
    processed = Column(Boolean, default=False)  # 是否已处理
    processing_error = Column(Text, nullable=True)  # 处理失败的错误信息

    # AI 处理结果（临时存储）
    extracted_titles = Column(Text, nullable=True)  # JSON: 提取的标题列表
    extracted_comments = Column(Text, nullable=True)  # JSON: 提取的评论列表

    # 时间戳
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=settings.inbox_retention_days)
    )

    def __repr__(self) -> str:
        return f"<InboxItem(id={self.id}, processed={self.processed})>"

    @property
    def is_expired(self) -> bool | ColumnElement[bool]:
        """检查是否已过期"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
