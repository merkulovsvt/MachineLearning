from datetime import datetime

from pydantic import BaseModel


class UserGet(BaseModel):
    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str

    class Config:
        # orm_mode = True - устарело
        from_attributes = True


class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        # orm_mode = True - устарело
        from_attributes = True


class FeedGet(BaseModel):
    user_id: int
    post_id: int

    action: str
    time: datetime

    user: UserGet
    post: PostGet

    class Config:
        # orm_mode = True - устарело
        from_attributes = True
