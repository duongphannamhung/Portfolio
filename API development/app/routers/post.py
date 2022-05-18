from fastapi import FastAPI, Response, status , HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM products""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(user_id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.post("/createposts")
# def get_posts(new_post: Post):
#     print(new_post.title)
#     return {"abc": "abc"}