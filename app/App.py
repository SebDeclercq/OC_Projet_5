#!/usr/bin/env python3
'''App class which is the main class of the program.

It pilots every actions for the P5 project, as it is the central
element of the entire program. Its main method is run() which
dertermines what action to do based on the Params object provided
while instanciating the App.'''
from typing import NoReturn, List, Dict, Optional, Any, Generator
import db.setup
from db import DB, DBCategory, DBProduct
from app import Params
from OpenFoodFacts import API, Product
from ui import UI, UIFactory
import yaml
import os


class App:
    '''Main application for OC P5

    Attributes:
        db: A DB instance used to interact with the database
        params: A Params instance used to configure the OC P5 actions'''
    db: DB
    params: Params

    def __init__(self, params: Params) -> None:
        '''Constructor'''
        self.params = params
        self._connect_db()

    def run(self) -> None:
        '''Central method starting up the App'''
        if self.params.interactive:
            self._interactive_mode()
        else:
            self._db_mode()
            if self.params.setup_db:
                print('Création de la base de données OK')
            elif self.params.update_db:
                print('Mise à jour de la base de données OK')

    def _db_mode(self) -> None:
        '''Private method used if the wished actions are
        database interaction like. Two options are available:
        1. Creating a new database (setup_db mode)
        2. Updating the database (update_db mode)'''
        self.api = API()
        categories = self._categories
        if self.params.setup_db:
            print('Cette opération va supprimer toutes les données '
                  'existantes. Continuer ?  [oN]')
            command: str = input('> ').lower()
            if command == 'o':
                db.setup.remove_all(self.params.db_uri)
            else:
                print('Abandon')
                exit()
            self._connect_db()  # Reconnect
        else:
            # Overwrites collected categories from YAML config file
            # Goal : update existing categories only without adding
            # a new one
            categories = [c.name for c in self.db.get_categories()]
        for category in categories:
            for product in self._search_api(category):
                self.db.add(product)

    @property
    def _categories(self) -> List[str]:
        '''Property method acting as a private attribute which
        contains the categories selected in the config file.'''
        with open(self.params.categories_file) as catego:
            data: Dict[str, Any] = yaml.load(catego)
        categories: List[str] = data['categories']
        self.max_products_by_category: int = data['max_products_by_category']
        if self.max_products_by_category > 100:
            # 100 products MAX by category
            self.max_nb_products_by_category = 100
        if len(categories) > 5:
            categories = categories[:4]  # 5 categories MAX
        return categories

    def _connect_db(self) -> DB:
        '''Private method to onnect to database with db attribute'''
        base, session = db.setup.start_up(self.params.db_uri)
        self.db = DB(base, session)
        return self.db

    def _search_api(self, category: str) \
            -> Generator[Product, None, None]:
        '''Private method collecting products by category with api attribute'''
        products: Generator[Product, None, None] = self.api.search(
            category, self.max_products_by_category
        )
        for product in products:
            product.categories = [category]
            yield product

    def _interactive_mode(self) -> None:
        ui: UI = UIFactory.factory(self.params.ui)
        ui.start(self)

    def get_categories(self) -> Generator[DBCategory, None, None]:
        '''Get all categories'''
        for category in self.db.get_categories():
            yield category

    def get_products(self, category_id: int) \
            -> Generator[DBProduct, None, None]:
        '''Get all products by category (id)'''
        products: List[DBProduct] = sorted(
            self.db.get_products_by_category(category_id),
            key=lambda p: (p.nutrition_grade, p.name), reverse=True
        )
        for product in products:
            yield product

    def get_product_details(self, product_id: int) -> DBProduct:
        '''Get a product details (by id)'''
        return self.db.get_product_by_id(product_id)

    def get_substitutes_for(self, product_id: int) \
            -> Generator[DBProduct, None, None]:
        '''Get substitues for a product (by id)'''
        for product in self.db.get_substitutes_for(product_id):
            yield product

    def add_favorite(self, substituted: DBProduct,
                     substituter: DBProduct) -> List[DBProduct]:
        '''Add a new favorite substitution (with id of the substitute
        and the substituted product) and returns both DBProducts'''
        return self.db.add_favorite(substituted, substituter)

    def get_favorite_products(self) -> Generator[DBProduct, None, None]:
        '''Get all saved products'''
        for favorite in self.db.get_favorite_products():
            yield favorite
