from datetime import date, timedelta

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
              title='FastAPI',
              description='Lesson9 API')


# @app.get("/")
# def index():
#     return 'hello, world'


@app.get("/")
def sum_int(a: int, b: int):
    return a + b


@app.get("/sum_date")
def sum_dates(current_date: date, offset: int):
    return current_date + timedelta(days=offset)


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: date


@app.post("/user/validate")
def user_validate(user: User):
    return f"Will add user: {user.name} {user.surname} with age {user.age}"


def get_db():
    connection = psycopg2.connect(
        host='postgres.lab.karpov.courses',
        port=6432,
        user='robot-startml-ro',
        password='pheiph0hahj1Vaif',
        database="startml",
        cursor_factory=RealDictCursor
    )
    return connection


@app.get("/user/{id}")
def get_user(id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            f"""
        SELECT gender, age, city
        FROM "user"
        WHERE id = {id}
        """
        )
        result = cursor.fetchone()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="user not found")


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        from_attributes = True


@app.get("/post/{id}", response_model=PostResponse)
def post_id(id: int, db=Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(
            f"""
        SELECT id, text, topic
        FROM post
        WHERE id = {id}
        """
        )
        result = cursor.fetchone()

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="user not found")
