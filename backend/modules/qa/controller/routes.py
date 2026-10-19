from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from shared.db import get_db
from modules.qa.service.qa_service import ask_question

router = APIRouter(prefix="/ask", tags=["qa"])


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


@router.post("")
async def ask(
    req: AskRequest,
    db: Session = Depends(get_db),
):
    """基于知识库内容回答用户问题（带溯源）"""
    return await ask_question(db, req.question, top_k=req.top_k)