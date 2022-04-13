from sqlalchemy import *
from config.database import Base

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))

    def __str__(self) -> str:
        return f"{self.name}"