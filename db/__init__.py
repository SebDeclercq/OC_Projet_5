#!/usr/bin/env python3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.sql.schema import ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
from .DB import DB

def name_for_many_to_many(base: DeclarativeMeta,
                          local_cls: DeclarativeMeta,
                          referred_cls: DeclarativeMeta,
                          constraint: ForeignKeyConstraint) -> str:
    if referred_cls.__name__[-1] == 'y':
        name = referred_cls.__name__[:-1] + 'ies'  # For category/categories
    else:
        name = referred_cls.__name__ + 's'
    return name.lower()


Base = automap_base()


def connect(_DB_URI: str) -> DB:
    engine = create_engine(_DB_URI)
    Base.prepare(engine, reflect=True,
                 name_for_collection_relationship=name_for_many_to_many)
    db = DB(Base, Session(engine))
    return db
