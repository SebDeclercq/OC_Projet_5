#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from db.setup import Base, IsSoldAt, repr_mixin


class Store(Base, repr_mixin):
    __tablename__ = 'Store'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    products = relationship('Product', secondary=IsSoldAt, backref='Store')
