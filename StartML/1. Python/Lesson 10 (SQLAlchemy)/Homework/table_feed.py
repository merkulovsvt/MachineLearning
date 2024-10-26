from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = 'feed_action'
    __table_args__ = {'schema': 'public'}

    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id, ondelete='CASCADE'), primary_key=True)

    action = Column(String)
    time = Column(DateTime)

    user = relationship(User)
    post = relationship(Post)
