# 评论路由
# 提供评论的 CRUD 接口

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# ========== 请求/响应模型 ==========

class CommentCreateRequest(BaseModel):
    """创建评论请求"""
    media_id: int
    content: str
    source: str = "user"  # user / ai / imported
    source_url: Optional[str] = None
    source_author: Optional[str] = None


class CommentResponse(BaseModel):
    """评论响应"""
    id: int
    media_id: int
    content: str
    source: str
    source_url: Optional[str]
    source_author: Optional[str]
    sentiment_score: Optional[float]
    created_at: datetime


class CommentListResponse(BaseModel):
    """评论列表响应"""
    items: List[CommentResponse]
    total: int


# ========== 路由端点 ==========

@router.get("/media/{media_id}", response_model=CommentListResponse)
async def get_media_comments(
    media_id: int,
    source: Optional[str] = Query(None, description="来源过滤: user/ai/imported"),
    limit: int = Query(50, ge=1, le=200, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
):
    """
    获取媒体的所有评论

    按时间倒序排列（论坛式展示）

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现评论列表查询"
    )


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(request: CommentCreateRequest):
    """
    创建评论

    创建后会：
    1. 触发情感分析
    2. 更新媒体的 mention_count
    3. 重新计算优先级分数

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现评论创建"
    )


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int):
    """
    获取单条评论

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现评论查询"
    )


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int):
    """
    删除评论

    删除后会重新计算媒体的优先级分数

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现评论删除"
    )


@router.post("/{media_id}/generate-summary")
async def generate_ai_summary(media_id: int):
    """
    为媒体生成 AI 总结评论

    基于已有评论生成总结性评论

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现 AI 总结生成"
    )
