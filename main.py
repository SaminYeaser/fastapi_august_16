from fastapi import FastAPI
from blog import model
from database import engine
from blog.routers import blog, user, authentication

app = FastAPI(
    title='My First API project'
)

model.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(blog.router)

app.include_router(user.router)

app.include_router(authentication.router)