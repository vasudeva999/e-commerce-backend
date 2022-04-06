from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

uri = "sqlite:///" + os.path.join(BASE_DIR, "../database.sqlite")

engine = create_engine(uri, echo=True, convert_unicode=True)

db_session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

Base = declarative_base()

Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)