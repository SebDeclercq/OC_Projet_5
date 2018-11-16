#!/usr/bin/env python3
"""Class interacting with the database of the App.

Has for purpose to handle all actions on the database (DDL, DML).
Built upon SQLAlchemy ORM."""
from sqlalchemy.orm import Session, Query
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from typing import NoReturn, List, Dict, Optional, Any, Generator, Union
from OpenFoodFacts import Product
from db.setup import (Product as DBProduct, Store as DBStore,
                      Category as DBCategory)


class DB:
    '''Class interacting with the database of the App.

    Attributes:
        base: the database itself
        session: the session connected to the database
        Product: the ORM Table for the Product table
        Store: the ORM Table for the Store table
        Category: the ORM Table for the Category table
    '''

    base: DeclarativeMeta
    session: Session
    Product: DeclarativeMeta
    Store: DeclarativeMeta
    Category: DeclarativeMeta

    def __init__(self, base: DeclarativeMeta, session: Session) -> None:
        '''Constructor'''
        self.base = base
        self.session = session
        self.Product = DBProduct
        self.Store = DBStore
        self.Category = DBCategory

    def add(self, product: Product) -> DBProduct:
        '''Method adding a new product to the database,
        including new store(s) and/or category(ies) if needed.
        Populates link tables too.
        Returns the new inserted DBProduct'''
        stores: List[DBStore] = self._add_stores(product.stores)
        categories: List[DBCategory] = self._add_categories(
            product.categories
        )
        query: Query = self.session.query(self.Product)
        existing_product: Optional[DBProduct] = query.filter(
            self.Product.id == product.id
        ).first()
        if existing_product:  # If a product exists, updates if
            new_product: DBProduct = self._update_product(
                existing_product, product, stores, categories
            )
        else:  # Else, inserts a new one
            new_product = self._add_product(product, stores, categories)
        try:
            self.session.commit()
            return new_product
        except Exception as err:
            self.session.rollback()
            raise err

    def _add_product(self, product: Product,
                     stores: List[DBStore],
                     categories: List[DBCategory]) -> DBProduct:
        '''Intermediate private method for better code segmentation.
        Inserts a new product in the Product table.
        Returns the new inserted DBProduct'''
        p: DBProduct = self.Product(
            id=product.id,
            name=product.name,
            nutrition_grade=product.nutrition_grades,
            url=product.url,
            stores=stores,
            categories=categories
        )
        self.session.add(p)
        return p

    def _add_stores(self, store_names: List[str]) -> List[DBStore]:
        '''For every store linked in the Product object,
        collects it if exists or creates a new one.
        Returns all the new DBStore objects.'''
        stores: List[DBStore] = []
        query: Query = self.session.query(self.Store)
        for store_name in store_names:
            existing_store: Optional[DBStore] = query.filter(
                    self.Store.name == store_name
            ).first()
            if not existing_store:
                store = self.Store(name=store_name)
                self.session.add(store)
                stores.append(store)
            else:
                stores.append(existing_store)
        return stores

    def _add_categories(self,
                        category_names: List[str]) -> List[DBCategory]:
        '''For every category linked in the Product object,
        collects it if exists or creates a new one.
        Returns all the new DBCategory objects.'''
        categories: List[DBCategory] = []
        query: Query = self.session.query(self.Category)
        for category_name in category_names:
            existing_category: Optional[DBCategory] = query.filter(
                self.Category.name == category_name
            ).first()
            if not existing_category:
                category = self.Category(name=category_name)
                self.session.add(category)
                categories.append(category)
            else:
                categories.append(existing_category)
        return categories

    def _update_product(self, existing_product: DBProduct,
                        product: Product, stores: List[DBStore],
                        categories: List[DBCategory]) -> DBProduct:
        '''If a DBProduct already exists in the database,
        updates it instead of inserting a new one.
        Returns the said DBProduct.'''
        existing_product.id = product.id
        existing_product.name = product.name
        existing_product.nutrition_grade = product.nutrition_grades
        existing_product.url = product.url
        existing_product.stores = stores
        existing_product.categories = categories
        return existing_product

    def get_categories(self) -> List[DBCategory]:
        '''Get all categories'''
        return self.session.query(self.Category)

    def get_products_by_category(self, category_id: int) -> List[DBProduct]:
        '''Get all products by category (id)'''
        return self.session.query(self.Category).filter(
            self.Category.id == category_id
        ).first().products

    def get_product_by_id(self, product_id: int) -> DBProduct:
        '''Get a product details (by id)'''
        return self.session.query(self.Product).filter(
            self.Product.id == product_id
        ).first()

    def get_substitutes_for(self, product_id: int) \
            -> List[DBProduct]:
        '''Get substitues for a product (by id)'''
        product: DBProduct = self.get_product_by_id(product_id)
        query: Query = self.session.query(self.Product).\
            filter(self.Product.nutrition_grade < product.nutrition_grade).\
            filter(self.Product.categories.any(id=product.categories[0].id)).\
            order_by(self.Product.nutrition_grade, self.Product.name)
        return query.all()

    def add_favorite(self, ids: List[int]) -> List[DBProduct]:
        '''Add a new favorite substitution (with id of the substitute
        and the substituted product) and returns both DBProducts'''
        substituted = self.get_product_by_id(ids[0])
        substituter = self.get_product_by_id(ids[1])
        substituted.substituted_by.append(substituter)
        substituter.substitutes.append(substituted)
        self.session.commit()
        return [substituted, substituter]

    def get_favorite_products(self) -> List[DBProduct]:
        '''Get all saved products'''
        return self.session.query(self.Product).filter(
            self.Product.substitutes.any(
                self.Product.id
            )
        ).all()
