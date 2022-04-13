from sqlalchemy import *
from config.database import Base
from auth.models import User
from sqlalchemy.orm import relationship, backref
from category.models import Category

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    price = Column(Float())
    description = Column(String(1000))
    quantity = Column(Integer())

    owner_id = Column(Integer, ForeignKey(User.id), nullable=False)
    owner = relationship(User, backref=backref('products', lazy=True))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    category = relationship(Category, backref=backref('products', lazy=True))

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"