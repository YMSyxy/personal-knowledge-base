from sqlalchemy import Column, String, Boolean
from shared.db import Base

class Folder(Base):
    __tablename__ = "folders"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    # 我们暂时不加复杂的关联表，先让它跑起来