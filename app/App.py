#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import db.setup
from db import DB, DBCategory, DBProduct
from app import Params
from OpenFoodFacts import API, Product
from ui import UI, UIFactory, UIReturn
import yaml
import os


class App:
    db: DB
    params: Params

    def __init__(self, params: Params) -> None:
        self.params = params
        self._connect_db()

    def run(self) -> None:
        if self.params.interactive:
            self._interactive_mode()
        else:
            self._db_mode()
            if self.params.setup_db:
                print('Création de la base de données OK')
            elif self.params.update_db:
                print('Mise à jour de la base de données OK')

    def _db_mode(self) -> None:
        self.api = API(verbose=self.params.verbose)
        categories = self._categories
        if self.params.setup_db:
            print('Cette opération va supprimer toutes les données '
                  'existantes. Continuer ?  [oN]')
            command: str = input('> ').lower()
            if command == 'o':
                if 'sqlite' in self.params.dbname:
                    db_filename = self.params.dbname[
                        self.params.dbname.find('///') + 3:
                    ]
                    os.remove(db_filename)
            else:
                print('Abandon')
                exit()
            self._connect_db()  # Reconnect
        else:
            # Overwrites collected categories from YAML config file
            categories = [c.name for c in self.db.get_categories()]
        for category in categories:
            for product in self._search_api(category):
                self.db.add(product)

    @property
    def _categories(self) -> List[str]:
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

    def _interactive_mode(self) -> Any:
        self.ui: UI = UIFactory.factory(self.params.ui)
        self.ui.display()
        while True:
            uir: UIReturn = self.ui.interact()
            data: Any = None
            if uir.message:
                print(uir.message)
            if uir.action == UI.QUIT:
                exit()
            elif uir.action == UI.S_LIST_CATEGO:
                data = [(c.name.capitalize(), c.id)
                        for c in self._get_categories()]
            elif uir.action == UI.S_LIST_PRODUCTS:
                if uir.id_query:
                    data = [(p.name.capitalize(), p.id)
                            for p in self._get_products(uir.id_query)]
            elif uir.action == UI.S_PRODUCT_PAGE:
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
                if uir.id_query:
                    substitutes: List[DBProduct] = self._get_substitutes_for(
                        uir.id_query
                    )
                    data = [(p.name.capitalize(), p.id) for p in substitutes]
            elif uir.action == UI.S_SAVED_FAVORITE:
                if uir.substitution_ids and len(uir.substitution_ids) == 2:
                    favorites: List[DBProduct] = self._add_favorite(
                        uir.substitution_ids
                    )
                    data = {
                        'substituted': favorites[0].name.capitalize(),
                        'substituter': favorites[1].name.capitalize(),
                    }
            elif uir.action == UI.F_LIST_FAVORITES:
                data = [(fav.name.capitalize(), fav.id)
                        for fav in self._get_favorite_products()]
            elif uir.action == UI.F_PRODUCT_PAGE:
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
            self.ui.display(data)

    def _get_categories(self) -> List[DBCategory]:
        return self.db.get_categories()

    def _get_products(self, category_id: int) -> List[DBProduct]:
        return self.db.get_products_by_category(category_id)

    def _get_product_details(self, product_id: int) -> DBProduct:
        return self.db.get_product_by_id(product_id)

    def _get_substitutes_for(self, product_id: int) -> List[DBProduct]:
        return self.db.get_substitutes_for(product_id)

    def _add_favorite(self, ids: List[int]) -> List[DBProduct]:
        return self.db.add_favorite(ids)

    def _get_favorite_products(self) -> List[DBProduct]:
        return self.db.get_favorite_products()
