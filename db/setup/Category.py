#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from db.setup import Base, HasCategory, repr_mixin


class Category(Base, repr_mixin):
    __tablename__ = 'Category'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(), nullable=False, unique=True)
    products = relationship('Product', secondary=HasCategory,
                            backref='Category')
