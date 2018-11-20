#!/usr/bin/env python3
'''UI in console'''
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform
from ..UI import UI
from ..UIReturn import UIReturn
from .Menu import Menu, MenuEntry
from app import App
from db import DBCategory, DBProduct


class ConsoleUI(UI):
    '''Class describing the UI in console.
    Inherits from the UI abstract class
    '''

    def __init__(self) -> None:
        text_file: str = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file, encoding='utf-8') as f:  # Get page contents
            self.contents: Dict[str, Any] = yaml.load(f)

    def start(self, app: App) -> None:
        self.app: App = app
        self.history: List[Any] = []
        print(self.contents['WELCOME'])
        self.top_menu()

    def quit(self) -> None:
        print('Au revoir !')
        exit()

    def top_menu(self) -> None:
        menu: Menu = Menu()
        menu.add(
            'Quel aliment souhaitez-vous remplacer ?',
            self.category_list_menu
        )
        menu.add(
            'Retrouver mes aliments substitués.',
            self.favorite_list_menu
        )
        self.interact(menu)

    def category_list_menu(self) -> None:
        print(self.contents['S_LIST_CATEGO'])
        menu: Menu = Menu()
        for category in self.app.get_categories():
            menu.add(
                category.name.capitalize(),
                self.product_list_menu,
                args=category.id
            )
        self.interact(menu)

    def favorite_list_menu(self) -> None:
        print(self.contents['F_LIST_FAVORITES'])
        menu: Menu = Menu()
        for favorite in self.app.get_favorite_products():
            menu.add(
                favorite.name.capitalize(),
                self.favorite_page,
                args=favorite.id
            )
        self.interact(menu)

    def product_list_menu(self, category_id: int) -> None:
        print(self.contents['S_LIST_PRODUCTS'])
        menu: Menu = Menu()
        for product in self.app.get_products(category_id):
            menu.add(
                product.name.capitalize(),
                self.product_page,
                args=product.id
            )
        self.interact(menu)

    def product_page(self, product_id: int) -> None:
        product: DBProduct = self.app.get_product_details(product_id)
        print(
            self.contents['S_PRODUCT_PAGE'] %
            {
                'id': product.id,
                'name': product.name.capitalize(),
                'nutrition_grade': product.nutrition_grade.upper(),
                'stores': ', '.join(
                    [s.name for s in product.stores]
                ),
                'url': product.url,
            }
        )
        menu: Menu = Menu()
        menu.add(
            'Trouver des substituts plus sains',
            self.substitute_list_menu,
            args=product_id
        )
        menu.add(
            'Sauvegarder dans les favoris',
            self.save_to_favorite
        )
        self.interact(menu)

    def favorite_page(self, product_id: int) -> None:
        product: DBProduct = self.app.get_product_details(product_id)
        print(
            self.contents['F_PRODUCT_PAGE'] %
            {
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
        )
        menu: Menu = Menu()
        self.interact(menu)

    def substitute_list_menu(self, product_id: int) -> None:
        print(self.contents['S_LIST_SUBSTITUTES'])
        menu: Menu = Menu()
        for product in self.app.get_substitutes_for(product_id):
            menu.add(
                product.name.capitalize(),
                self.product_page,
                args=product.id
            )
        if not menu.entries:
            print('Aucun substitut trouvé !\n')
        self.interact(menu)

    def save_to_favorite(self) -> None:
        ...

    def interact(self, menu: Menu) -> Any:
        action: MenuEntry = self._get_next_action(menu)
        if action.args:
            action.handler(action.args)
        else:
            action.handler()

    def _get_next_action(self, menu: Menu) -> MenuEntry:
        menu.add("Retour à l'accueil", self.top_menu, 0)
        menu.add('Quitter', self.quit, 'q')
        while True:
            for entry in menu.entries.values():
                print(entry)
            action = input('> ').lower().rstrip()
            if action in menu.entries:
                return menu.entries[action]
            else:
                print(f'Action "{action}" inconnue')
