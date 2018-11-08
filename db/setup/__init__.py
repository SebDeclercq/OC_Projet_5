#!/usr/bin/env python3
from sqlalchemy import (Table, Column, Integer, ForeignKey,
                        PrimaryKeyConstraint, create_engine)
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from typing import Tuple


class repr_mixin:
    def __repr__(self) -> str:
        self.__dict__.pop('_sa_instance_state')
        return str(self.__dict__)


Base = declarative_base()


def start_up(_DB_URI: str = 'sqlite:///:memory:') \
                -> Tuple[DeclarativeMeta, Session]:
    engine = create_engine(_DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return (Base, Session())


IsSoldAt: Table = Table(
    'IsSoldAt', Base.metadata,
    Column('product_id', Integer(), ForeignKey('Product.id'), nullable=False),
    Column('store_id', Integer(), ForeignKey('Store.id'), nullable=False),
    PrimaryKeyConstraint('product_id', 'store_id')
)

HasCategory: Table = Table(
    'HasCategory', Base.metadata,
    Column('product_id', Integer(), ForeignKey('Product.id'), nullable=False),
    Column('category_id', Integer(), ForeignKey('Category.id'),
           nullable=False),
    PrimaryKeyConstraint('product_id', 'category_id')
)

from .Product import Product
from .Store import Store
from .Category import Category
