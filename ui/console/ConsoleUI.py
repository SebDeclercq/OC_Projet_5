#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform


class ConsoleUI:
    WELCOME: int = 1
    TOP_MENU: int = 2
    GO_BACK_TO_TOP_MENU: int = 0
    S_LIST_CATEGO: int = 3  # S_ for "substitute"
    S_LIST_PRODUCTS: int = 4
    S_PRODUCT_PAGE: int = 5
    F_LIST_FAVORITES: int = 6  # F_ for "favorite"
    F_PRODUCT_PAGE: int = 7

    def __init__(self) -> None:
        self.current_level = self.WELCOME
        self.page_contents: Dict[int, str] = {}
        text_file = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file) as f:
            text: Dict[str, str] = yaml.load(f)
        for page_name, page_content in text.items():
            page_level = getattr(self, page_name)
            self.page_contents[page_level] = page_content

    def display(self) -> Any:
        if self.current_level == self.WELCOME:
            print(self.page_contents[self.WELCOME])
            self.current_level = self.TOP_MENU
        print(self.page_contents[self.current_level])
        if self.current_level != self.TOP_MENU:
            print("0 - Retour à l'accueil\n")

    def interact(self) -> Any:
        command: str = input('> ').lower()
        if command in ('q', 'quit', 'e', 'exit'):
            print('Bye !')
            exit()
        else:
            if not command.isdigit():
                print('Veuillez saisir un chiffre présent dans le menu')
            else:
                action: int = int(command)
            if action == self.GO_BACK_TO_TOP_MENU:
                self.current_level = self.WELCOME
            elif self.current_level == self.TOP_MENU:
                if action == 1:
                    self.current_level = self.S_LIST_CATEGO
                    return
                elif action == 2:
                    self.current_level = self.S_LIST_PRODUCTS
                else:
                    self._print_error(action)
                    return False
            elif self.current_level == self.S_PRODUCT_PAGE:
                ...
            elif self.current_level == self.F_LIST_FAVORITES:
                ...
            elif self.current_level == self.F_PRODUCT_PAGE:
                ...
            else:
                self._print_error(action)

    def _print_error(self, action: int) -> None:
        print('Action %d inconnue' % action)
        print('Veuillez saisir un chiffre présent dans le menu')

    def _clear_screen(self) -> None:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
