#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import db.setup
from db import DB
from app import Params
from OpenFoodFacts import API, Product
import yaml


class App:
    db: DB
    params: Params

    def __init__(self, params: Params) -> None:
        self.params = params

    def run(self) -> None:
        self._connect_db()
        self.api = API(verbose=self.params.verbose)
        for category in self._get_categories():
            for product in self._search_api(category):
                self.db.add(product)

    def _get_categories(self) -> List[str]:
        with open(self.params.categories_file) as catego:
            data: Dict[str, Any] = yaml.load(catego)
        self.categories: List[str] = data['categories']
        self.max_products_by_category: int = data['max_products_by_category']
        if self.max_products_by_category > 100:
            # 100 products MAX by category
            self.max_nb_products_by_category = 100
        if len(self.categories) > 5:
            self.categories = self.categories[:4]  # 5 categories MAX
        return self.categories

    def _connect_db(self) -> DB:
        base, session = db.setup.start_up(self.params.dbname)
        self.db = DB(base, session)
        return self.db

    def _search_api(self, category: str) \
            -> Generator[Product, None, None]:
        products: Generator[Product, None, None] = self.api.search(
            category, self.max_products_by_category
        )
        for product in products:
            product.categories = [category]
            yield product
