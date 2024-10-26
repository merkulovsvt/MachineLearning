from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = ("postgresql://"
                           "robot-startml-ro:"  # username
                           "pheiph0hahj1Vaif@"  # password
                           "postgres.lab.karpov.courses:"  # host
                           "6432/"  # port
                           "startml"  # db
                           )

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
