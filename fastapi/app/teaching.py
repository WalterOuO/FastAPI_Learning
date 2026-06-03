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


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


'''
Method 0: Basic FastAPI
'''


# '''
# When we send a POST request to create a new post, 
# we need to include the title and content of the post in the request body. 
# We can use the Body function from FastAPI to extract the data from the request body and use it to create a new post. 
# The new post will be added to the my_posts list and returned in the response.
# '''
# @app.post("/posts")
# def create_posts(bodymessage: dict = Body(...)):
#     print(bodymessage)
#     return {"new_post": f"title: {bodymessage['title']}, content: {bodymessage['content']}  "}



# '''
# Method 1: Using in-memory data structure (a list of dicts) to perform CRUD operations without connecting to a database.
# '''


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
#             {"title": "favorite foods", "content": "I like pizza", "id": 2}]


# def find_post(id):
#     for i, post in enumerate(my_posts):
#         if post['id'] == id:
#             return i, post
#     return None, None


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


    
# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: schemas.PostCreate):
#     post_dict = post.model_dump()           # post.model_dump() is the meaning of post.dict(): change post into a dictionary. 
#                                             # post.dict() is only in pydantic v1, now pydantic v2 use post.model_dump() instead.
#     post_dict['id'] = randrange(0, 1000000)
    
#     my_posts.append(post_dict)
#     return {"data": post_dict}


# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return {"latest_post": post}


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):  # 手動設定 Error 的回應status code時 才需要引入 response這個參數
#                                             # 不然使用HTTPException就會自動幫我們設定status code, 不需要再引入 response來設定一次
#     _, post = find_post(id)
#     if not post:
        
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id: {id} was not found"}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     return {"post_detail": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index, _ = find_post(id)
    
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

#     # When sending 204 status code, we should not return any content in the response body. So we can just return an empty Response with the appropriate status code.

# @app.put("/posts/{id}")
# def update_post(id: int, post: schemas.PostCreate):
#     index, _ = find_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     # initallize a new dict
#     post_dict = post.model_dump()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {"data": post_dict}



# '''
# Method 2: Using psycopg2 to connect to the database and perform CRUD operations with raw SQL queries.
# '''

# # Using psycopg2 to connect to the database
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='PostgreSQL', cursor_factory=RealDictCursor)
        
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)
#         time.sleep(2)



# @app.get("/posts", response_model=list[schemas.Post])
# def get_posts():
#     with conn.cursor() as cursor:                # Recommand build cursor for all router to let cursor work idependently
#         cursor.execute("""SELECT * FROM posts""")
#         posts = cursor.fetchall()
#     # posts = db.query(models.Post).all()
#     return posts


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post: schemas.PostCreate):
#     with conn.cursor() as cursor:
#         cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                     (post.title, post.content, post.published))
#         new_post = cursor.fetchone()
#         conn.commit()   # commit the transaction to save the changes to the database
#     # new_post = models.Post(**post.dict())
#     # db.add(new_post)
#     # db.commit()
#     # db.refresh(new_post)
#     return new_post


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     with conn.cursor() as cursor:
#         cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#         post = cursor.fetchone()
#     # post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     return post


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     with conn.cursor() as cursor:
#         cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#         deleted_post = cursor.fetchone()
#         conn.commit()
#     # deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
#     # db.delete(deleted_post)
#     # db.commit()
    
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # When sending 204 status code, we should not return any content in the response body. 
#     # So we can just return an empty Response with the appropriate status code.


# @app.put("/posts/{id}")
# def update_post(id: int, post: schemas.PostCreate):
#     with conn.cursor() as cursor:
#         cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                        (post.title, post.content, post.published, str(id)))
#         updated_post = cursor.fetchone()
#         conn.commit()
#     # post_query = db.query(models.Post).filter(models.Post.id == id)
#     # updated_post = post_query.first()

#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     # post_query.update(post.model_dump(), synchronize_session=False)     # update出去要是dict，所以post.model_dump()
#     # db.commit()
#     # db.refresh(updated_post)    
#     return updated_post




'''
Method 3: Using SQLAlchemy ORM to connect to the database and perform CRUD operations.
'''

models.Base.metadata.create_all(bind=engine)


# This is a  sqlalchemy test endpoint, we can use it to test if the connection to the database is successful.
# @app.post("/sqlalchemy")
# def test_post(post_data: schemas.PostCreate, db: SessionDep):
    
    
#     posts = db.query(models.Post).all()
#     return {"data": posts}


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: SessionDep):
    
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: SessionDep):
    
    new_post = models.Post(**post.model_dump()) # post.model_dump() is post.dict(), models.Post 把它會打包成資料庫規定的物件
    db.add(new_post)
    db.commit()             # 資料確實已寫入database裡面了
    db.refresh(new_post)    # 讓 database把自動遞增的 id、預設的時間戳記 created_at等欄位的值更新到 new_post 這個物件裡面
    return new_post

#   **post.model_dump( ) 的用法
# data = post.model_dump()
# new_post = models.Post(title=data["title"], content=data["content"], published=data["published"])   原本要一個一個自己指定欄位
# new_post = models.Post(**post.model_dump())  **會直接把字典裡的 key-value pair 直接傳給 models.Post 的建構子


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: SessionDep):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    post_query.delete(synchronize_session=False)    # False表示不需要同步刪除SQLAlchemy 記憶體「快取區（Session）」中的檔案，反正刪掉也不會用了。
    # db.delete(deleted_post)                       # post_query.delete是直接從資料庫刪除, db.delete會從databse撈出來再刪 (浪費再撈的效能)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: SessionDep):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)     # update出去要是dict，所以post.model_dump()
    db.commit()
    db.refresh(updated_post)
    
    return updated_post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: SessionDep):
    
    # hash the password before saving it to the database
    hashed_pwd = utils.hash_password(user.password)
    
    user_data = user.model_dump()
    user_data['password'] = hashed_pwd
    
    # Store into the database
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user 


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: SessionDep):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} was not found")
    return user
    


