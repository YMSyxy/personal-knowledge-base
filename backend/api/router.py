from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import uuid4

from shared.db import get_db
from modules.ingest.service.splitter import split_markdown
from modules.ingest.repository.document_repo import save_document
from modules.ingest.domain.models import Document, Chunk
from modules.retrieve.service.search import search

# 注意：qa 已经没了，全在这里
from modules.agent.service.agent_service import ask_question
from modules.manage.service.folder_service import get_all_folders, create_folder

api_router = APIRouter()

# ==================== 1. 知识收录 ====================
@api_router.post("/documents/upload", tags=["ingest"])
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="目前只支持 Markdown 文件")
    content = (await file.read()).decode("utf-8")
    doc_id = str(uuid4())
    
    # 这里暂时写死，以后从参数传
    doc = Document(id=doc_id, title=file.filename, source_type="md", is_public=False)
    
    chunks_text = split_markdown(content)
    chunks = [
        Chunk(id=str(uuid4()), document_id=doc_id, content=text, embedding=None, chunk_index=i) 
        for i, text in enumerate(chunks_text)
    ]
    save_document(db, doc, chunks)
    return {"id": doc_id, "title": doc.title, "chunks_count": len(chunks)}

# ==================== 2. 知识检索 ====================
@api_router.get("/search", tags=["retrieve"])
async def search_docs(q: str = Query(...), top_k: int = 5, db: Session = Depends(get_db)):
    return search(db, q, top_k=top_k)

# ==================== 3. 文件夹管理 ====================
class FolderCreate(BaseModel):
    name: str

@api_router.get("/folders", tags=["manage"])
async def list_folders(db: Session = Depends(get_db)):
    return get_all_folders(db)

@api_router.post("/folders", tags=["manage"])
async def add_folder(req: FolderCreate, db: Session = Depends(get_db)):
    return create_folder(db, req.name)

# ==================== 4. Agent 智能问答 ====================
class AskRequest(BaseModel):
    question: str
    top_k: int = 3

@api_router.post("/agent/ask", tags=["agent"])
async def agent_chat(req: AskRequest, db: Session = Depends(get_db)):
    return await ask_question(db, req.question, req.top_k)