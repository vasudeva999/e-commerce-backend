from sqlalchemy import *
from config.database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100))
    last_login = Column(DateTime)
    first_name = Column(String(50))
    last_name = Column(String(50))

    def __str__(self):
        return f"{self.username}"