from fastapi import FastAPI, HTTPException, Response, status, APIRouter
from .. import models, schemas, utils
from ..database import SessionDep


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: SessionDep):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} was not found")
    return user