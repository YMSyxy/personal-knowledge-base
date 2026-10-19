from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 新增

from shared.db import init_db
from modules.ingest.controller.routes import router as ingest_router
from modules.retrieve.controller.routes import router as retrieve_router
from modules.qa.controller.routes import router as qa_router

app = FastAPI(title="Personal Knowledge Base")

# 新增 CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(ingest_router)
app.include_router(retrieve_router)
app.include_router(qa_router)

@app.get("/health")
def health():
    return {"status": "ok"}