#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform
from ..UI import UI
from ..UIReturn import UIReturn


class ConsoleUI(UI):
    def __init__(self) -> None:
        self.current_level = self.WELCOME
        self.page_contents: Dict[int, str] = {}
        text_file = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file) as f:
            text: Dict[str, str] = yaml.load(f)
        for page_name, page_content in text.items():
            page_level = getattr(self, page_name)
            self.page_contents[page_level] = page_content.rstrip()

    def display(self, data: Any = None) -> Any:
        if self.current_level == self.WELCOME:
            print(self.page_contents[self.WELCOME])
            self.current_level = self.TOP_MENU
        print(self.page_contents[self.current_level])
        if data:
            self.actions: Dict[int, int] = {}
            list_menus: List[int] = [self.S_LIST_CATEGO,
                                     self.S_LIST_PRODUCTS,
                                     self.F_LIST_FAVORITES]
            product_pages: List[int] = [self.S_PRODUCT_PAGE,
                                        self.F_PRODUCT_PAGE]
            if self.current_level in list_menus:
                for idx, element in enumerate(data):
                    no_el: int = idx + 1
                    print('%s - %s' % (str(no_el), element[0]))
                    self.actions[no_el] = element[1]
            elif self.current_level in product_pages:
                print(self.page_contents[self.current_level] % data)
        if self.current_level != self.TOP_MENU:
            print("0 - Retour à l'accueil")
        print("q - Quitter")

    def interact(self) -> UIReturn:
        ret: UIReturn = UIReturn()
        command: str = input('> ').lower()
        if command in ('q', 'quit', 'e', 'exit'):
            ret.message = 'Bye !'
            ret.action = self.QUIT
        else:
            if not command.isdigit():
                ret.message = self._error(command)
                return ret
            else:
                action: int = int(command)
            if action == self.GO_BACK_TO_TOP_MENU:
                self.current_level = self.WELCOME
            elif self.current_level == self.TOP_MENU:
                if action == 1:
                    self.current_level = self.S_LIST_CATEGO
                    ret.action = self.S_LIST_CATEGO
                elif action == 2:
                    self.current_level = self.F_LIST_FAVORITES
                else:
                    ret.message = self._error(action)
            elif self.current_level == self.S_LIST_CATEGO:
                self.current_level = self.S_LIST_PRODUCTS
                ret.action = self.S_LIST_PRODUCTS
                ret.id_query = self.actions[action]
            elif self.current_level == self.S_LIST_PRODUCTS:
                self.current_level = self.S_PRODUCT_PAGE
                ret.action = self.S_PRODUCT_PAGE
                ret.id_query = self.actions[action]
            elif self.current_level == self.S_PRODUCT_PAGE:
                ...
            elif self.current_level == self.F_PRODUCT_PAGE:
                ...
            else:
                ret.message = self._error(action)
        return ret

    def _error(self, action: Union[str, int]) -> str:
        message: str = 'Action %s inconnue' % action
        message += '\nVeuillez saisir un chiffre présent dans le menu'
        return message

    def _clear_screen(self) -> None:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
