#!/usr/bin/env python3
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from typing import NoReturn, List, Dict, Optional, Any, Generator
from OpenFoodFacts import Product
import db.setup


class DB:
    def __init__(self, base: DeclarativeMeta, session: Session) -> NoReturn:
        self.base: DeclarativeMeta = base
        self.session: Session = session
        if hasattr(self.base, 'classes'):
            self.Product: DeclarativeMeta = self.base.classes.Product
            self.Store: DeclarativeMeta = self.base.classes.Store
            self.Category: DeclarativeMeta = self.base.classes.Category
        else:
            self.Product: DeclarativeMeta = db.setup.Product
            self.Store: DeclarativeMeta = db.setup.Store
            self.Category: DeclarativeMeta = db.setup.Category

    def add(self, product: Product) -> bool:
        stores = self._add_stores(product.stores)
        categories = self._add_categories(product.categories)
        self._add_product(product, stores, categories)
        try:
            self.session.commit()
            return True
        except Exception as err:
            print(str(err))
            self.session.rollback()
            return False

    def _add_product(self, product: Product,
                     stores: List[db.setup.Store],
                     categories: List[db.setup.Category]) -> int:
        p: db.setup.Product = self.Product(
            id=product.id,
            name=product.name,
            # brands=product.brands,
            nutrition_grade=product.nutrition_grades,
            url=product.url,
            stores=stores,
            categories=categories
        )
        self.session.add(p)
        return p.id

    def _add_stores(self, store_names: List[str]) -> List[db.setup.Store]:
        stores: List[db.setup.Store] = []
        for store_name in store_names:
            store = self._add_store(store_name)
            stores.append(store)
        return stores

    def _add_store(self, store_name: str) -> db.setup.Store:
        store = self.Store(name=store_name)
        self.session.add(store)
        return store

    def _add_categories(self, category_names: List[str]) \
                            -> List[db.setup.Category]:
        categories: List[db.setup.Category] = []
        for category_name in category_names:
            category = self._add_category(category_name)
            categories.append(category)
        return categories

    def _add_category(self, category_name: str) -> db.setup.Category:
        category = self.Category(name=category_name)
        self.session.add(category)
        return category
