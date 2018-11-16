#!/usr/bin/env python3
'''Class defining the Category Table in the database'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from db.setup import Base, HasCategory, repr_mixin


class Category(Base, repr_mixin):
    '''Class defining the Category Table in the database

    Attributes:
        id:       The id Column
        name:     The name Column
        products: A relationship containing every DBProducts linked
                  to the category through the HasCategory link table'''
    __tablename__ = 'Category'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship('Product', secondary=HasCategory,
                            backref='Category')
