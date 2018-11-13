#!/usr/bin/env python3
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship, backref
from db.setup import (Base, IsSoldAt, HasCategory,
                      IsFavoriteSubstituteOf, repr_mixin)


class Product(Base, repr_mixin):
    __tablename__ = 'Product'

    id = Column(BigInteger(), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)
    url = Column(String(255), nullable=False)
    stores = relationship('Store', secondary=IsSoldAt, backref='Product')
    categories = relationship('Category', secondary=HasCategory,
                              backref='Product')
    substituted_by = relationship(
        'Product', secondary=IsFavoriteSubstituteOf,
        primaryjoin=id == IsFavoriteSubstituteOf.c.substituted_product_id,
        secondaryjoin=id == IsFavoriteSubstituteOf.c.substitute_product_id,
        backref='SubtituteProduct'
    )
    substitutes = relationship(
        'Product', secondary=IsFavoriteSubstituteOf,
        primaryjoin=id == IsFavoriteSubstituteOf.c.substitute_product_id,
        secondaryjoin=id == IsFavoriteSubstituteOf.c.substituted_product_id,
        backref='SubtitutedProduct'
    )
