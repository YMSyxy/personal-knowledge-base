import re

import jieba
from sqlalchemy.orm import Session

from modules.ingest.domain.models import Chunk
from modules.retrieve.repository import chunk_repo


def tokenize(query: str) -> list[str]:
    """
    把 query 拆成关键词：
    - jieba 分词（中文）
    - 过滤掉单字、标点、停用词
    """
    # jieba 分词
    words = jieba.lcut(query)

    # 过滤：长度 >= 2，且不是纯标点
    stop_words = {"的", "了", "是", "在", "和", "与", "什么", "怎么", "为什么", "如何"}
    keywords = []
    for w in words:
        w = w.strip()
        if len(w) < 2:
            continue
        if w in stop_words:
            continue
        if re.fullmatch(r"[\W_]+", w):  # 纯标点
            continue
        keywords.append(w)

    return keywords


def search(db: Session, query: str, top_k: int = 5) -> dict:
    """
    检索入口：
    1. query 分词
    2. 关键词检索
    3. 返回结果（带 chunk 信息）
    """
    keywords = tokenize(query)

    if not keywords:
        return {"query": query, "keywords": [], "results": []}

    chunks = chunk_repo.search_by_keywords(db, keywords, top_k=top_k)

    results = [
        {
            "chunk_id": c.id,
            "document_id": c.document_id,
            "content": c.content,
            "chunk_index": c.chunk_index,
        }
        for c in chunks
    ]

    return {
        "query": query,
        "keywords": keywords,
        "results": results,
    }