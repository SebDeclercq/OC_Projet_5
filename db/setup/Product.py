#!/usr/bin/env python3
'''Class defining the Product Table in the database'''
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship, backref
from db.setup import (Base, IsSoldAt, HasCategory,
                      IsFavoriteSubstituteOf, repr_mixin)


class Product(Base, repr_mixin):
    '''Class defining the Category Table in the database

    Attributes:
        id:              The id Column
        name:            The name Column
        nutrition_grade: The nutrition_grade Column ("nutriscore")
        url:             The url Column (link to the OpenFoodFacts Web page
                         for the product)
        stores:          A relationship containing every DBStores linked
                         to the product through the IsSoldAt link table
        categories:      A relationship containing every DBCategories linked
                         to the product through the HasCategory link table
        substituted_by:  A relationship containing every DBProducts linked
                         to the product through the IsFavoriteSubstituteOf
                         link table (contains the substituter products)
        substitutes:     A relationship containing every DBProducts linked
                         to the product through the IsFavoriteSubstituteOf
                         link table (contains the substituted products)
        '''
    __tablename__ = 'Product'

    id = Column(BigInteger(), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    nutrition_grade = Column(String(1), nullable=False)
    url = Column(String(255), nullable=False)
    stores = relationship('Store', secondary=IsSoldAt, backref='Product')
    categories = relationship('Category', secondary=HasCategory,
                              backref='Product')
    substituted_by = relationship(  # From substituted to substituter
        'Product', secondary=IsFavoriteSubstituteOf,
        primaryjoin=id == IsFavoriteSubstituteOf.c.substituted_product_id,
        secondaryjoin=id == IsFavoriteSubstituteOf.c.substitute_product_id,
        backref='SubtituteProduct'
    )
    substitutes = relationship(  # From substituter to substituted
        'Product', secondary=IsFavoriteSubstituteOf,
        primaryjoin=id == IsFavoriteSubstituteOf.c.substitute_product_id,
        secondaryjoin=id == IsFavoriteSubstituteOf.c.substituted_product_id,
        backref='SubtitutedProduct'
    )
