#!/usr/bin/env python3
"""Package file setting up environment for the database's class.
It doesn't respect the PEP8 due to SQLAlchemy bad adequation of it.
This package file is intended to clean up the database's other class files.
"""
from sqlalchemy import (Table, Column, Integer, BigInteger,
                        ForeignKey, create_engine)
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from typing import Tuple


class repr_mixin:
    '''Mixin class created to share the same __repr__() method
    to the DB objects'''
    def __repr__(self) -> str:
        self.__dict__.pop('_sa_instance_state')
        return str(self.__dict__)


Base: DeclarativeMeta = declarative_base()  # Instanciate DB


def start_up(_DB_URI: str) -> Tuple[DeclarativeMeta, Session]:
    '''Function creating the engine and session for the DB
    Returns the base and the session.'''
    engine = create_engine(_DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return (Base, Session())


def remove_all(_DB_URI: str) -> None:
    '''Function creating the engine for the DB and drops all tables'''
    engine = create_engine(_DB_URI)
    Base.metadata.drop_all(engine)


# Instanciate link table between Product and Store
IsSoldAt: Table = Table(
    'IsSoldAt', Base.metadata,
    Column('product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('store_id', Integer(), ForeignKey('Store.id'),
           nullable=False, primary_key=True)
)

# Instanciate link table between Product and Category
HasCategory: Table = Table(
    'HasCategory', Base.metadata,
    Column('product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('category_id', Integer(), ForeignKey('Category.id'),
           nullable=False, primary_key=True)
)

# Instanciate link table between Product (to substitute)
# and Product (substituter)
IsFavoriteSubstituteOf: Table = Table(
    'IsFavoriteSubstituteOf', Base.metadata,
    Column('substitute_product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True),
    Column('substituted_product_id', BigInteger(), ForeignKey('Product.id'),
           nullable=False, primary_key=True)
)

# Finally imports the Table Class
# This occurs at the end of the package file because
# previous data are required for them to work fine
# (the Base and Table objects).
from .Product import Product
from .Store import Store
from .Category import Category
