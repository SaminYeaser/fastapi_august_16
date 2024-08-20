from fastapi import APIRouter, Depends, status, HTTPException
from blog import schemas,model
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user

router = APIRouter(
    prefix= "/blog",
   tags=['Blogs'],
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def creatBlog(request: schemas.Blog,db: Session = Depends(get_db),):
    newBlog = model.Blog(title = request.title,body= request.body,user_id=1)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

@router.get('/',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,)
def getAllBlog(db: Session = Depends(get_db),current_user : schemas.User = Depends(get_current_user)):
    blogs = db.query(model.Blog).all()
    return blogs


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,)
def getSpecificId(id: int, db: Session = Depends(get_db)):
    specificId = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not specificId:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The blog with this ID not found')
    return specificId

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def deleteBlog(id,db: Session = Depends(get_db)):
    deletedBlog = db.query(model.Blog).filter(model.Blog.id == id)
    
    if not deletedBlog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The blog with this ID not found')
    deletedBlog.delete(synchronize_session=False)
    db.commit()
    return {
        'code': status.HTTP_200_OK,
        'message':'Blog Deleted'
    }

@router.put('/{id}', status_code=status.HTTP_200_OK)
def updateBlog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    updatedBlog = db.query(model.Blog).filter(model.Blog.id == id)
    
    if not updatedBlog.first():
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The blog with this ID not found')
    updatedBlog.update(dict(request))
    db.commit()
    return {
        'code': status.HTTP_200_OK,
        'message':'Blog updated'
    }