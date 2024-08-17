from fastapi import FastAPI
from blog.schemas import Blog
from typing import Optional
from blog import schemas,model
from database import SessionLocal, engine

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/blog/{id}')
def about(id : int):
    return { 'data' : id}

@app.get('/blog/comments/{id}')
def about(id):
    return { 'data' : ['1','2']}

@app.get('/blog')
def about(limit = 10, published: bool = True, sort : Optional[str] = None):
    if published:
        return {'data': f'{limit} blogs published sort {sort}'}
    else:
        return {'data': f'Total {limit} blogs total sort {sort}'}
    





@app.post('/blog')
def creatBlog(request: Blog):
    return {'data':f'A blog created in the name of {request.title}', }