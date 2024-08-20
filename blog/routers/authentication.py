from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from .. import schemas, model
from database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from hasing_pass import verfiyPassword
import jwt_token
from datetime import datetime, timedelta, timezone
from typing import Annotated

router = APIRouter(
    tags=['Authentication'],
    prefix='/login'
)

@router.post('/')

def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db : Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user found')
    if not verfiyPassword(request.password , user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password not matched')
    access_token_expires = timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



