#!/usr/bin/env python3
from sqlalchemy import (Table, Column, Integer, BigInteger,
                       ForeignKey, create_engine)
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from typing import Tuple


class repr_mixin:
    def __repr__(self) -> str:
        self.__dict__.pop('_sa_instance_state')
        return str(self.__dict__)


Base = declarative_base()


def start_up(_DB_URI: str) -> Tuple[DeclarativeMeta, Session]:
    engine = create_engine(_DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return (Base, Session())


def remove_all(_DB_URI: str) -> None:
    engine = create_engine(_DB_URI)
    Base.metadata.drop_all(engine)


IsSoldAt: Table = Table(
    'IsSoldAt', Base.metadata,
    Column('product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('store_id', Integer(), ForeignKey('Store.id'),
           nullable=False, primary_key=True)
)

HasCategory: Table = Table(
    'HasCategory', Base.metadata,
    Column('product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('category_id', Integer(), ForeignKey('Category.id'),
           nullable=False, primary_key=True)
)

IsFavoriteSubstituteOf: Table = Table(
    'IsFavoriteSubstituteOf', Base.metadata,
    Column('substitute_product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('substituted_product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True)
)

from .Product import Product
from .Store import Store
from .Category import Category
