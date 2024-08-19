from fastapi import FastAPI, Depends, status, Response, HTTPException
from blog.schemas import Blog
from typing import Optional
from blog import schemas,model
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app = FastAPI(
    title='My First API project'
)

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get('/blog/{id}')
# def about(id : int):
#     return { 'data' : id}

# @app.get('/blog/comments/{id}')
# def about(id):
#     return { 'data' : ['1','2']}

# @app.get('/blog')
# def about(limit = 10, published: bool = True, sort : Optional[str] = None):
#     if published:
#         return {'data': f'{limit} blogs published sort {sort}'}
#     else:
#         return {'data': f'Total {limit} blogs total sort {sort}'}
    



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['Blogs'])
def creatBlog(request: schemas.Blog,db: Session = Depends(get_db)):
    newBlog = model.Blog(title = request.title,body= request.body,user_id=1)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

@app.get('/blog',status_code=status.HTTP_200_OK,tags=['Blogs'])
def getAllBlog(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blogs'])
def getSpecificId(id: int, db: Session = Depends(get_db)):
    specificId = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not specificId:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The blog with this ID not found')
    return specificId

@app.delete('/blog/{id}', status_code=status.HTTP_200_OK,tags=['Blogs'])
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

@app.put('/blog/{id}', status_code=status.HTTP_200_OK,tags=['Blogs'])
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



# Users
@app.put('/user',response_model=schemas.ShowUser ,status_code=status.HTTP_201_CREATED,tags=['Users'])
def createUser(request: schemas.User,db: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashedPassword = pwd_context.hash(request.password)
    newUser = model.User(name = request.name, email= request.email, password=hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser


@app.get('/user',status_code=status.HTTP_200_OK,tags=['Users'])
def getAllUsers(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users

@app.get('/user/{email}',response_model=schemas.ShowUser,status_code=status.HTTP_200_OK,tags=['Users'])
def getSpecificUser(email: str,db: Session = Depends(get_db)):
    specificUser = db.query(model.User).filter(model.User.email == email).first()
    if not specificUser:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return specificUser