from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter
from typing import Optional
from .. import models, schemas, utils, oauth2
from ..database import SessionDep


router = APIRouter(
    prefix="/posts",    # 當下面所有router 都以 /posts 開頭，就可加prefix，不用每個router再寫一次 /posts 了
    tags=["Posts"]      # 這個 tags 是用來在 http://127.0.0.1:8000/docs 文件裡面把相關的 API 分類在一起的，讓文件更有組織性和可讀性
)

@router.get("/", response_model=list[schemas.Post])
def get_posts(db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    print(current_user.email)
    # post_data = post.model_dump()
    # post_data['owner_id'] = current_user.id
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()          
    db.refresh(new_post)
    
    return new_post


@router.get("/latest")
def get_latest_post(db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")   
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)
    
    return updated_post