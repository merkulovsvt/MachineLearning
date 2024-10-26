import datetime
from typing import List

import psycopg2
from fastapi import FastAPI, HTTPException
from loguru import logger
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


# uvicorn app:app --reload - для запуска сервера
class BookingGet(BaseModel):
    user_id: int
    post_id: int
    action: str
    time: datetime.datetime

    class Config:
        from_attributes = True


class SimpleUser(BaseModel):
    name: str
    surname: str
    age: int


@app.get("/", summary="Just say hello   ")
def say_hello():
    '''
    Say hello to a user
    '''
    return "hello"


@app.get("/sum")
def sum_two(a: int, b: int) -> int:
    return a + b


@app.get("/print/{number1}/{number2}")
def print_num(number1: int, number2: int) -> int:
    return number1 * 2 + number2 * 2


@app.post("/user")
def print(name: str) -> dict:
    return {'message': f'hello {name}'}


@app.get("/bookings/all", response_model=List[BookingGet])
def all_bookings():
    connection = psycopg2.connect(
        host='postgres.lab.karpov.courses',
        port=6432,
        user='robot-startml-ro',
        password='pheiph0hahj1Vaif',
        database="startml",
        cursor_factory=RealDictCursor
    )

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM "feed_action"
        LIMIT 10
        """
    )

    result = cursor.fetchall()
    logger.info(result)

    cursor.close()
    connection.close()
    return result


@app.post("/user/validate")
def validate_user(user: SimpleUser):
    logger.info(user.dict())
    return "ok"


@app.get("/error")
def check_error(a: int):
    if a == 5:
        raise HTTPException(status_code=304)
    else:
        return "ok"
