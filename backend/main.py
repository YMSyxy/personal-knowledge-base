from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.db import init_db
from api.router import api_router  # 统一路由收口

app = FastAPI(title="Personal Knowledge Base")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# 统一注册，前缀 /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}