from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from shared.db import get_db
from modules.retrieve.service.search import search

router = APIRouter(prefix="/search", tags=["retrieve"])


@router.get("")
async def search_documents(
    q: str = Query(..., description="检索查询"),
    top_k: int = Query(5, ge=1, le=20, description="返回数量"),
    db: Session = Depends(get_db),
):
    """关键词检索：输入 query，返回相关 chunks"""
    return search(db, q, top_k=top_k)