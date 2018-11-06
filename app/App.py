#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
from sqlalchemy.orm import Session
import db.setup
from db import Base
from app import Params
from OpenFoodFacts import API, Product


class App:
    session: Session
    params: Params

    def __init__(self, params: Params) -> NoReturn:
        self.params = params

    def run(self) -> NoReturn:
        self._connect_db()
        for product in self._do_api_request():
            print(product)

    def _connect_db(self) -> Session:
        if self.params.setup_db or self.params.dbname == 'sqlite:///:memory:':
            self.session = db.setup.start_up(self.params.dbname)
        else:
            self.session = db.connect(self.params.dbname)
        return self.session

    def _do_api_request(self) -> Generator[Product, None, None]:
        if self.params.search is not None:
            products: Generator[Product, None, None] = API.simple_search(
                self.params.search
            )
        elif self.params.tag is not None:
            if self.params.category is not None:
                products = API.search_by_category(self.params.tag)
            ...
        for product in products:
            yield product
