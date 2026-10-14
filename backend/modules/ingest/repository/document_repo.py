from sqlalchemy.orm import Session

from modules.ingest.domain.models import Document, Chunk


def save_document(db: Session, doc: Document, chunks: list[Chunk]) -> Document:
    """保存文档及其 chunks"""
    db.add(doc)
    for chunk in chunks:
        db.add(chunk)
    db.commit()
    db.refresh(doc)
    return doc


def get_document(db: Session, doc_id: str) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()


def list_documents(db: Session, limit: int = 50) -> list[Document]:
    return db.query(Document).order_by(Document.created_at.desc()).limit(limit).all()


def delete_document(db: Session, doc_id: str) -> bool:
    doc = get_document(db, doc_id)
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True