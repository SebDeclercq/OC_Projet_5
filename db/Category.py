#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from db import Base, HasCategory, repr_mixin


class Category(Base, repr_mixin):
    __tablename__ = 'Category'

    id = Column(Integer(), autoincrement=True,
                primary_key=True, nullable=False)
    name = Column(String(), nullable=False)
