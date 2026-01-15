# 收集箱路由
# 提供内容粘贴和处理接口

from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# ========== 请求/响应模型 ==========

class InboxSubmitRequest(BaseModel):
    """提交内容到收集箱"""
    content: str  # 粘贴的文本内容
    url: Optional[str] = None  # 可选的原始 URL


class InboxItemResponse(BaseModel):
    """收集箱条目响应"""
    id: int
    raw_content: str
    url: Optional[str]
    processed: bool
    processing_error: Optional[str]
    extracted_titles: Optional[List[str]]
    created_at: datetime
    expires_at: datetime


class InboxProcessResult(BaseModel):
    """处理结果响应"""
    success: bool
    message: str
    created_media_ids: List[int]  # 新创建的媒体条目 ID
    updated_media_ids: List[int]  # 更新的媒体条目 ID
    errors: List[str]


# ========== 路由端点 ==========

@router.post("/submit", response_model=InboxItemResponse, status_code=status.HTTP_201_CREATED)
async def submit_to_inbox(request: InboxSubmitRequest):
    """
    提交内容到收集箱

    流程：
    1. 保存原始内容到 Inbox
    2. 异步触发 AI 分析
    3. 返回 Inbox 条目 ID

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现内容提交"
    )


@router.get("/", response_model=List[InboxItemResponse])
async def list_inbox_items(
    processed: Optional[bool] = Query(None, description="过滤处理状态"),
    limit: int = Query(50, ge=1, le=100, description="返回数量"),
):
    """
    获取收集箱列表

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现收集箱列表查询"
    )


@router.get("/{inbox_id}", response_model=InboxItemResponse)
async def get_inbox_item(inbox_id: int):
    """
    获取单个收集箱条目

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现收集箱条目查询"
    )


@router.post("/{inbox_id}/process", response_model=InboxProcessResult)
async def process_inbox_item(inbox_id: int):
    """
    手动触发处理收集箱条目

    流程：
    1. 调用 AI 分析内容
    2. 提取标题和评论
    3. 查询是否已存在条目（RAG/向量搜索）
    4. 创建或更新媒体条目
    5. 更新评分
    6. 标记为已处理

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现收集箱处理"
    )


@router.delete("/{inbox_id}")
async def delete_inbox_item(inbox_id: int):
    """
    删除收集箱条目

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现收集箱删除"
    )


@router.post("/cleanup")
async def cleanup_expired_items():
    """
    清理过期的收集箱条目

    TODO: 实现具体逻辑
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: 实现过期清理"
    )
