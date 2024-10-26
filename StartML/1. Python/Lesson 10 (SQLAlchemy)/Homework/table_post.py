from sqlalchemy import Column, Integer, String

from database import Base
from database import SessionLocal


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)


if __name__ == "__main__":
    # session = SessionLocal()
    with SessionLocal() as session:
        result = session.query(Post). \
            filter(Post.topic == 'business'). \
            order_by(Post.id.desc()). \
            limit(10)

        print([post.id for post in result])
