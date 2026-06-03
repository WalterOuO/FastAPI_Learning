from random import randrange

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sklearn.utils import deprecated
from . import models, schemas, utils
from .database import engine, SessionDep
from .routers import post, user, auth
from .config import settings 


# After using Alembic to manage database migrations, we don't need to use0 SQLAlchemy's create_all() method anymore
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# middleware 是一種在 request 和 response 之間執行的函式，可以用來處理跨域請求、驗證、日誌記錄等功能
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]             # 允許所有來源的請求，這裡可以根據需要修改為特定的域名或 IP 地址, ex: ["https://google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


