from fastapi import APIRouter, Depends, status, HTTPException
from blog import schemas,model
from sqlalchemy.orm import Session
from database import get_db
from hasing_pass import hashingPassword

router = APIRouter(
    prefix="/user",
    tags=['Users']

)

@router.put('/',response_model=schemas.ShowUser ,status_code=status.HTTP_201_CREATED)
def createUser(request: schemas.User,db: Session = Depends(get_db)):
    
    newUser = model.User(name = request.name, email= request.email, password=hashingPassword(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@router.get('/',status_code=status.HTTP_200_OK)
def getAllUsers(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users

@router.get('/{email}',response_model=schemas.ShowUser,status_code=status.HTTP_200_OK)
def getSpecificUser(email: str,db: Session = Depends(get_db)):
    specificUser = db.query(model.User).filter(model.User.email == email).first()
    if not specificUser:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return specificUser