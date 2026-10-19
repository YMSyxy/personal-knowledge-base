from sqlalchemy.orm import Session

from modules.ingest.domain.models import Chunk


def search_by_keywords(db: Session, keywords: list[str], top_k: int = 5) -> list[Chunk]:
    """
    关键词检索：对每个关键词做 LIKE 匹配，去重后返回。
    简单版：不考虑相关度排序（用 Python 再算）。
    """
    if not keywords:
        return []

    # 所有关键词 OR 起来查
    from sqlalchemy import or_
    conditions = [Chunk.content.like(f"%{kw}%") for kw in keywords]
    chunks = db.query(Chunk).filter(or_(*conditions)).all()

    # Python 里算命中数排序
    def hit_count(chunk: Chunk) -> int:
        return sum(1 for kw in keywords if kw in chunk.content)

    chunks.sort(key=hit_count, reverse=True)
    return chunks[:top_k]