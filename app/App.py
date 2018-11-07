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
            nb_product = 0
            for product in self._do_api_request(category):
                self.db.add(product)
                nb_product += 1
                if nb_product > 100:  # 100 products MAX by category
                    break

    def _get_categories(self) -> List[str]:
        with open(self.params.categories_file) as catego:
            self.categories: List[str] = yaml.load(catego)
        if len(self.categories) > 5:
            self.categories = self.categories[:4]  # 5 categories MAX
        return self.categories

    def _connect_db(self) -> DB:
        base, session = db.setup.start_up(self.params.dbname)
        self.db = DB(base, session)
        return self.db

    def _do_api_request(self, category: str) \
            -> Generator[Product, None, None]:
        for product in self.api.search_by_category(category):
            product.categories = [category]
            yield product
