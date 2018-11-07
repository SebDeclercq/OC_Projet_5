#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import db.setup
from db import DB
from app import Params
from OpenFoodFacts import API, Product


class App:
    db: DB
    params: Params

    def __init__(self, params: Params) -> None:
        self.params = params

    def run(self) -> None:
        self._connect_db()
        self.api = API(verbose=self.params.verbose)
        for product in self._do_api_request():
            self.db.add(product)
            # print(product)

    def _connect_db(self) -> DB:
        base, session = db.setup.start_up(self.params.dbname)
        self.db = DB(base, session)
        return self.db

    def _do_api_request(self) -> Generator[Product, None, None]:
        if self.params.search is not None:
            products: Generator[Product, None, None] = self.api.simple_search(
                self.params.search
            )
        elif self.params.tag is not None:
            if self.params.category is not None:
                products = self.api.search_by_category(self.params.tag)
            ...
        for product in products:
            yield product
