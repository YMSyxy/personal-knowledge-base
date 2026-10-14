from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from shared.db import get_db
from modules.ingest.domain.models import Document, Chunk
from modules.ingest.service.splitter import split_markdown
from modules.ingest.repository import document_repo

router = APIRouter(prefix="/documents", tags=["ingest"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """上传 Markdown 文件 → 切分 → 存库"""
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="目前只支持 Markdown 文件")

    content = (await file.read()).decode("utf-8")
    doc_id = str(uuid4())

    doc = Document(
        id=doc_id,
        title=file.filename,
        source_type="md",
        source_url=None,
    )

    chunks_text = split_markdown(content)
    chunks = [
        Chunk(
            id=str(uuid4()),
            document_id=doc_id,
            content=text,
            embedding=None,
            chunk_index=i,
        )
        for i, text in enumerate(chunks_text)
    ]

    document_repo.save_document(db, doc, chunks)
    return {
        "id": doc_id,
        "title": doc.title,
        "chunks_count": len(chunks),
    }


@router.get("/{doc_id}")
async def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = document_repo.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": doc.id,
        "title": doc.title,
        "source_type": doc.source_type,
        "created_at": doc.created_at,
        "chunks_count": len(doc.chunks),
    }


@router.get("")
async def list_documents(db: Session = Depends(get_db)):
    docs = document_repo.list_documents(db)
    return [
        {"id": d.id, "title": d.title, "source_type": d.source_type}
        for d in docs
    ]