from sqlalchemy.orm import Session
from modules.manage.domain.models import Folder
from uuid import uuid4

def create_folder(db: Session, name: str):
    folder = Folder(id=str(uuid4()), name=name)
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder

def get_all_folders(db: Session):
    folders = db.query(Folder).all()
    if not folders:
        return [{"id": "default", "name": "我的第一个收藏夹"}]
    return [{"id": f.id, "name": f.name} for f in folders]