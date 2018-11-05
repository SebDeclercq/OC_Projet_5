#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from db import Base, IsSoldAt, HasCategory, repr_mixin


class Product(Base, repr_mixin):
    __tablename__ = 'Product'

    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)
    url = Column(String(), nullable=False)
    stores = relationship('Store', secondary=IsSoldAt, backref='Product')
