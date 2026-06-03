from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from ..database import SessionDep
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
# if 前端 用 JSON send the login data as , we can use this:
# def login(db: SessionDep, user_credentials: schemas.UserLogin):

# if 前端 用 form-data send the login data as , we should use this:
def login(db: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    # OAuth2PasswordRequestForm 預設欄位是 username、password 解析出來，所以要用email 對應 username
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    
    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # return token    
    
    return {"access_token": access_token, "token_type": "bearer"} 