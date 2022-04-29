import datetime

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from .base import Base



class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)    


class Product(Base):
    __tablename__ = "product"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id, ondelete="SET NULL"), nullable=True)
    brand_id = Column(Integer, ForeignKey(Brand.id, ondelete="CASCADE"))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False)
    category = relationship(Category, primaryjoin=category_id == Category.id)
    brand = relationship(Brand, primaryjoin=brand_id == Brand.id)
