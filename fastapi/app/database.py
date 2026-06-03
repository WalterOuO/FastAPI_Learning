from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import Depends
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

# 1. 建立引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. 宣告模型基底類別的方式
class Base(DeclarativeBase):
    pass

# 3. FastAPI 建立資料庫連線的 Dependency
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]