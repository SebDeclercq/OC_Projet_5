#!/usr/bin/env python3
from sqlalchemy import (Table, Column, Integer, String,
                        ForeignKey, PrimaryKeyConstraint, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
from typing import NoReturn
import sys


Base = declarative_base()


class repr_mixin:
    def __repr__(self) -> str:
        return str(self.__dict__)


IsSoldIn = Table(
    'IsSoldIn', Base.metadata,
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


class Product(Base, repr_mixin):
    __tablename__ = 'Product'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)
    url = Column(String(), nullable=False)
    stores = relationship('Store', secondary=IsSoldIn, backref='Product')


class Store(Base, repr_mixin):
    __tablename__ = 'Store'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(), nullable=False)
    products = relationship('Product', secondary=IsSoldIn, backref='Store')


class Category(Base, repr_mixin):
    __tablename__ = 'Category'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(), nullable=False)


if len(sys.argv) > 1:
    dbname = sys.argv[1]
else:
    dbname = ':memory:'
engine = create_engine('sqlite:///' + dbname)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
