#!/usr/bin/env python3
'''UI in console'''
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform
from ..UI import UI
from .Menu import Menu, MenuEntry
from app import App
from db import DBCategory, DBProduct


class ConsoleUI(UI):
    '''Class describing the UI in console.
    Inherits from the UI abstract class

    Attributes:
        app: The Running App
        contents: Holds the text to display page by page
        history: Contains the previous products in the current sequence
    '''

    def __init__(self) -> None:
        '''Constructor getting page contents automatically'''
        text_file: str = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file, encoding='utf-8') as f:  # Get page contents
            self.contents: Dict[str, Any] = yaml.load(f)

    def start(self, app: App) -> None:
        '''Main access method, launch the App UI'''
        self.app: App = app
        self.history: List[DBProduct] = []
        print(self.contents['WELCOME'])
        self.top_menu()

    def quit(self) -> None:
        '''Quits'''
        print('Au revoir !')
        exit()

    def top_menu(self) -> None:
        '''Actions and display for the top menu'''
        self.history.clear()  # Clears history every time we meet the top
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
        '''Actions and display for the categories list menu'''
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
        '''Actions and display for the favorites list menu'''
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
        '''Actions and display for the products list menu'''
        print(self.contents['S_LIST_PRODUCTS'])
        menu: Menu = Menu()
        for product in self.app.get_products(category_id):
            text_option: str = (
                '(NUTRISCORE: %s) %-50s'
                % (product.nutrition_grade.upper(), product.name.capitalize())
            )
            menu.add(
                text_option,
                self.product_page,
                args=product.id
            )
        self.interact(menu)

    def product_page(self, product_id: int) -> None:
        '''Actions and display for the product details page'''
        product: DBProduct = self.app.get_product_details(product_id)
        self.history.append(product)  # Adds seen product to history
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
        '''Actions and display for the favorite product details page'''
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
            text_option: str = (
                '(NUTRISCORE: %s) %-50s'
                % (product.nutrition_grade.upper(), product.name.capitalize())
            )
            menu.add(
                text_option,
                self.product_page,
                args=product.id
            )
        if not menu.entries:
            print('Aucun substitut trouvé !\n')
        self.interact(menu)

    def save_to_favorite(self) -> None:
        '''Actions and display for the saving module'''
        if not len(self.history) >= 2:
            print('Ce produit est le premier visionné, '
                  'vous ne pouvez pas sauvegarder de substitut.')
            previous_product_id: int = self.history.pop().id
            self.product_page(previous_product_id)
        favorites: List[DBProduct] = self.app.add_favorite(
            *self.history[-2:]
        )
        print(
            self.contents['S_SAVED_FAVORITE'] %
            {
                'substituted': favorites[0].name.capitalize(),
                'substituter': favorites[1].name.capitalize(),
            }
        )
        menu: Menu = Menu()
        self.interact(menu)

    def interact(self, menu: Menu) -> Any:
        '''Main interaction method, piloting the actions for every menus'''
        action: MenuEntry = self._get_next_action(menu)
        if action.args:
            action.handler(action.args)
        else:
            action.handler()

    def _get_next_action(self, menu: Menu) -> MenuEntry:
        '''Method waiting for user input, returning next chosen action'''
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
