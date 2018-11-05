#!/usr/bin/env python3
from sqlalchemy import (Table, Column, Integer, ForeignKey,
                        PrimaryKeyConstraint, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional, Any


class repr_mixin:
    def __repr__(self) -> str:
        return str(self.__dict__)

Base = declarative_base()

def start_up(_DB_URI: Optional[str] = ':memory:') -> Any:
    engine = create_engine('sqlite:///' + _DB_URI)
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

IsSoldAt = Table(
    'IsSoldAt', Base.metadata,
    Column('product_id', Integer(), ForeignKey('Product.id'), nullable=False),
    Column('store_id', Integer(), ForeignKey('Store.id'), nullable=False),
    PrimaryKeyConstraint('product_id', 'store_id')
)

HasCategory = Table(
    'HasCategory', Base.metadata,
    Column('product_id', Integer(), ForeignKey('Product.id'), nullable=False),
    Column('category_id', Integer(), ForeignKey('Category.id'),
           nullable=False),
    PrimaryKeyConstraint('product_id', 'category_id')
)

from .Product import Product
from .Store import Store
from .Category import Category
