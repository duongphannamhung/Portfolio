from fastapi import FastAPI, Response, status , HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

class Post(BaseModel):
    title: str
    content: str

while True:
    try:
        conn = psycopg2.connect(host="localhost", database='fastapi',user='postgres',password="Rindothuy256oik",cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connect was succesfull!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "success"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)