from fastapi import FastAPI

from shared.db import init_db
from modules.ingest.controller.routes import router as ingest_router
from modules.retrieve.controller.routes import router as retrieve_router
from modules.qa.controller.routes import router as qa_router

app = FastAPI(title="Personal Knowledge Base")

# 启动时建表
init_db()

# 注册路由
app.include_router(ingest_router)
app.include_router(retrieve_router)
app.include_router(qa_router)


@app.get("/health")
def health():
    return {"status": "ok"}