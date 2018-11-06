#!/usr/bin/env python3
from sqlalchemy.orm import Session, Query
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from typing import NoReturn, List, Dict, Optional, Any, Generator
from OpenFoodFacts import Product
from db.setup import (Product as DBProduct, Store as DBStore,
                     Category as DBCategory)


class DB:
    def __init__(self, base: DeclarativeMeta, session: Session) -> NoReturn:
        self.base: DeclarativeMeta = base
        self.session: Session = session
        self.Product: DeclarativeMeta = DBProduct
        self.Store: DeclarativeMeta = DBStore
        self.Category: DeclarativeMeta = DBCategory

    def add(self, product: Product) -> int:
        stores = self._add_stores(product.stores)
        categories = self._add_categories(product.categories)
        query: Query = self.session.query(self.Product)
        existing_product: Optional[DBProduct] = query.filter(
            self.Product.id == product.id
        ).first()
        if existing_product:
            product_id: int = self._update_product(
                existing_product, product, stores, categories
            )
        else:
            product_id = self._add_product(product, stores, categories)
        try:
            self.session.commit()
            return product_id
        except Exception as err:
            self.session.rollback()
            raise err

    def _add_product(self, product: Product,
                     stores: List[DBStore],
                     categories: List[DBCategory]) -> int:
        p: DBProduct = self.Product(
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

    def _add_stores(self, store_names: List[str]) -> List[DBStore]:
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

    def _add_categories(self, category_names: List[str]) \
                            -> List[DBCategory]:
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
                        categories: List[DBCategory]) -> int:
        existing_product.id = product.id
        existing_product.name = product.name
        # existing_product.brands = product.brands
        existing_product.nutrition_grade = product.nutrition_grades
        existing_product.url = product.url
        existing_product.stores = stores
        existing_product.categories = categories
        return existing_product.id
