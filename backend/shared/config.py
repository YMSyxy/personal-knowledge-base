import os

# 开发阶段用 SQLite，生产环境计划迁移到 PostgreSQL + pgvector
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pkb.db")

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")