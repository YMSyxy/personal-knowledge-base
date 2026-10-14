from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import DATABASE_URL

# SQLite 需要 check_same_thread=False，允许多线程访问
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    """建表：导入所有模型后调用 create_all"""
    # 导入模型，让 Base 知道有哪些表
    from modules.ingest.domain import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI 依赖：每个请求一个 session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()