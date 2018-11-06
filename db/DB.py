#!/usr/bin/env python3
from sqlalchemy.orm import Session, Query
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
        query: Query = self.session.query(self.Product)
        existing_product: Optional[db.setup.Product] = query.filter(
            self.Product.id == product.id
        ).first()
        if existing_product:
            return True
        else:
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
        query: Query = self.session.query(self.Store)
        for store_name in store_names:
            existing_store: Optional[db.setup.Store] = query.filter(
                    self.Store.name == store_name
            ).first()
            if not existing_store:
                store = self.Store(name=store_name)
                self.session.add(store)
                stores.append(store)
            else:
                stores.append(existing_store)
        return stores

    def _add_categories(self, category_names: List[str]) \
                            -> List[db.setup.Category]:
        categories: List[db.setup.Category] = []
        query: Query = self.session.query(self.Category)
        for category_name in category_names:
            existing_category: Optional[db.setup.Category] = query.filter(
                self.Category.name == category_name
            ).first()
            if not existing_category:
                category = self.Category(name=category_name)
                self.session.add(category)
                categories.append(category)
            else:
                categories.append(existing_category)
        return categories
