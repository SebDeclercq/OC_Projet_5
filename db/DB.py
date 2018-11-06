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
        for store in product.stores:
            self._add_store(store)
        try:
            self.session.commit()
            return True
        except Exception as err:
            print(str(err))
            self.session.rollback()
            return False

    def _add_store(self, store_name: str) -> int:
        store = self.Store(name=store_name)
        self.session.add(store)
        return store.id
