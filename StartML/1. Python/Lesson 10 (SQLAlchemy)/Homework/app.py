from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import desc, func

from database import SessionLocal
from schema import UserGet, PostGet, FeedGet
from table_feed import Feed
from table_post import Post
from table_user import User

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
              title='SQLAlchemy API',
              description='Lesson10 API')


def get_db():
    with SessionLocal() as session:
        return session


@app.get('/user/{id}', response_model=UserGet, tags=['User'])
def get_user_by_id(id: int, session=Depends(get_db)):
    result = session.query(User). \
        where(User.id == id). \
        one_or_none()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get('/post/{id}', response_model=PostGet, tags=['Post'])
def get_post_by_id(id: int, session=Depends(get_db)):
    result = session.query(Post). \
        where(Post.id == id). \
        one_or_none()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Post not found")


@app.get('/user/{id}/feed', response_model=List[FeedGet], tags=['User'])
def get_feed_by_user_id(id: int, limit=10, session=Depends(get_db)):
    result = session.query(Feed). \
        where(Feed.user_id == id). \
        order_by(desc(Feed.time)). \
        limit(limit). \
        all()

    return result


@app.get('/post/{id}/feed', response_model=List[FeedGet], tags=['Post'])
def get_feed_by_user_id(id: int, limit=10, session=Depends(get_db)):
    result = session.query(Feed). \
        where(Feed.post_id == id). \
        order_by(desc(Feed.time)). \
        limit(limit). \
        all()

    return result


@app.get('/post/recommendations/', response_model=List[PostGet], tags=['FinalProject'])
def get_recommended_feed(id: int, limit=10, session=Depends(get_db)):
    result = session.query(Post.id, Post.text, Post.topic). \
        select_from(Feed). \
        where(Feed.action == 'like'). \
        join(Post). \
        group_by(Post.id). \
        order_by(desc(func.count())). \
        limit(limit).all()

    return result
