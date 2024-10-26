from sqlalchemy import Column, Integer, String, func, desc

from database import Base, SessionLocal


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == '__main__':
    with SessionLocal() as session:
        result = session.query(User.country.label("user_country"),
                               User.os.label("user_os"),
                               func.count().label("user_count")). \
            where(User.exp_group == 3). \
            group_by(User.country, User.os). \
            having(func.count() > 100). \
            order_by(desc("user_count")). \
            all()
    print(result)
