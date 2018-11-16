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
from ui import UI, UIFactory, UIReturn
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
        self.api = API(verbose=self.params.verbose)
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

    def _interactive_mode(self) -> Any:
        '''Private method piloting user interaction.
        This method relies on the content of a UIReturn object,
        which contains diversed data, depending on the current
        state of the UI.'''
        self.ui: UI = UIFactory.factory(self.params.ui)
        self.ui.display()
        while True:  # Until asked, never stop
            uir: UIReturn = self.ui.interact()
            data: Any = None
            if uir.message:  # If there's a message to display
                print(uir.message)
            if uir.action == UI.QUIT:  # If exit asked
                exit()
            elif uir.action == UI.S_LIST_CATEGO:
                # If the list of categories is needed,
                # returns their names (for display) and ids
                # (for further interaction)
                data = [(c.name.capitalize(), c.id)
                        for c in self._get_categories()]
            elif uir.action == UI.S_LIST_PRODUCTS:
                # If the list of products is needed,
                # returns their names (for display) and ids
                # (for further interaction)
                if uir.id_query:
                    data = [(p.name.capitalize(), p.id)
                            for p in self._get_products(uir.id_query)]
            elif uir.action == UI.S_PRODUCT_PAGE:
                # If the details of a product is needed,
                # collects them with its id, converts the data
                # to the needed format and returns it
                if uir.id_query:
                    product: DBProduct = self._get_product_details(
                        uir.id_query
                    )
                    data = {
                        'id': product.id,
                        'name': product.name.capitalize(),
                        'nutrition_grade': product.nutrition_grade.upper(),
                        'stores': ', '.join(
                            [s.name for s in product.stores]
                        ),
                        'url': product.url,
                    }
            elif uir.action == UI.S_LIST_SUBSTITUTES:
                # If the list of substitues is needed,
                # collects them with the id of the product to substitute
                # and returns their names (for display) and ids
                # (for further interaction)
                if uir.id_query:
                    substitutes: List[DBProduct] = self._get_substitutes_for(
                        uir.id_query
                    )
                    data = [(p.name.capitalize(), p.id) for p in substitutes]
            elif uir.action == UI.S_SAVED_FAVORITE:
                # For saving a new favorite substitution,
                # the ids of the substituted product and its
                # substitute is required. Returns both names.
                if uir.substitution_ids and len(uir.substitution_ids) == 2:
                    favorites: List[DBProduct] = self._add_favorite(
                        uir.substitution_ids
                    )
                    data = {
                        'substituted': favorites[0].name.capitalize(),
                        'substituter': favorites[1].name.capitalize(),
                    }
            elif uir.action == UI.F_LIST_FAVORITES:
                # If the list of favorites is needed,
                # collects them with the id of the product to substitute
                # and returns their names (for display) and ids
                # (for further interaction)
                data = [(fav.name.capitalize(), fav.id)
                        for fav in self._get_favorite_products()]
            elif uir.action == UI.F_PRODUCT_PAGE:
                # If the details of a product is needed,
                # collects them with its id, converts the data
                # to the needed format and returns it
                if uir.id_query:
                    product = self._get_product_details(
                        uir.id_query
                    )
                    data = {
                        'id': product.id,
                        'name': product.name.capitalize(),
                        'nutrition_grade': product.nutrition_grade.upper(),
                        'stores': ', '.join(
                            [s.name for s in product.stores]
                        ),
                        'url': product.url,
                        'substitutes': '\n'.join(
                            ['- ' + p.name + ' (NUTRISCORE: '
                                + p.nutrition_grade.upper() + ')'
                                for p in product.substitutes]
                        ),
                    }
            # Displays refreshed "page" with optional data
            self.ui.display(data)

    def _get_categories(self) -> List[DBCategory]:
        '''Get all categories'''
        return self.db.get_categories()

    def _get_products(self, category_id: int) -> List[DBProduct]:
        '''Get all products by category (id)'''
        return self.db.get_products_by_category(category_id)

    def _get_product_details(self, product_id: int) -> DBProduct:
        '''Get a product details (by id)'''
        return self.db.get_product_by_id(product_id)

    def _get_substitutes_for(self, product_id: int) -> List[DBProduct]:
        '''Get substitues for a product (by id)'''
        return self.db.get_substitutes_for(product_id)

    def _add_favorite(self, ids: List[int]) -> List[DBProduct]:
        '''Add a new favorite substitution (with id of the substitute
        and the substituted product) and returns both DBProducts'''
        return self.db.add_favorite(ids)

    def _get_favorite_products(self) -> List[DBProduct]:
        '''Get all saved products'''
        return self.db.get_favorite_products()
