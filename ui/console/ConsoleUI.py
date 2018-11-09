#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform
from ..UI import UI
from ..UIReturn import UIReturn


class ConsoleUI(UI):
    def __init__(self) -> None:
        self.current_level: int = self.WELCOME
        self.page_contents: Dict[int, str] = {}
        self.list_menus: List[int] = [
            self.S_LIST_CATEGO, self.S_LIST_PRODUCTS,
            self.S_LIST_SUBSTITUTES, self.F_LIST_FAVORITES
        ]
        self.product_pages: List[int] = [
            self.S_PRODUCT_PAGE, self.F_PRODUCT_PAGE, self.S_SAVED_FAVORITE
        ]
        self.history: Any = []
        text_file: str = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file, encoding='utf-8') as f:
            text: Dict[str, str] = yaml.load(f)
        for page_name, page_content in text.items():
            page_level = getattr(self, page_name)
            self.page_contents[page_level] = page_content.rstrip()

    def display(self, data: Any = None) -> Any:
        if self.current_level == self.WELCOME:
            print(self.page_contents[self.WELCOME])
            self.current_level = self.TOP_MENU
        if self.current_level not in self.product_pages:
            print(self.page_contents[self.current_level])
        if data:
            if self.current_level in self.list_menus:
                actions: Dict[int, int] = {}
                for idx, element in enumerate(data):
                    no_el: int = idx + 1
                    print('%s - %s' % (str(no_el), element[0]))
                    actions[no_el] = element[1]
                self.history.append(actions)
            elif self.current_level in self.product_pages:
                print(self.page_contents[self.current_level] % data)
                if 'id' in data:
                    self.history.append(data['id'])
        else:
            if self.current_level in self.list_menus:
                print('\nAucun résultat trouvé\n')
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
                self.history = []  # Clear history every time you meet the top
            elif self.current_level == self.TOP_MENU:
                if action == 1:
                    self.current_level = self.S_LIST_CATEGO
                    ret.action = self.S_LIST_CATEGO
                elif action == 2:
                    self.current_level = self.F_LIST_FAVORITES
                    ret.action = self.F_LIST_FAVORITES
                else:
                    ret.message = self._error(action)
            elif self.current_level == self.S_LIST_CATEGO:
                self.current_level = self.S_LIST_PRODUCTS
                ret.action = self.S_LIST_PRODUCTS
                ret.id_query = self.history[-1][action]
            elif self.current_level == self.S_LIST_PRODUCTS:
                self.current_level = self.S_PRODUCT_PAGE
                ret.action = self.S_PRODUCT_PAGE
                ret.id_query = self.history[-1][action]
            elif self.current_level == self.S_PRODUCT_PAGE:
                if action == 1:
                    self.current_level = self.S_LIST_SUBSTITUTES
                    ret.action = self.S_LIST_SUBSTITUTES
                    ret.id_query = self.history[-1]
                elif action == 2:
                    self.current_level = self.S_SAVED_FAVORITE
                    ret.action = self.S_SAVED_FAVORITE
                    ret.substitution_ids = []
                    for p_id in (self.history[-3], self.history[-1]):
                        if isinstance(p_id, int):
                            ret.substitution_ids.append(p_id)
                    if len(ret.substitution_ids) != 2:
                        ...
            elif self.current_level == self.S_LIST_SUBSTITUTES:
                self.current_level = self.S_PRODUCT_PAGE
                ret.action = self.S_PRODUCT_PAGE
                ret.id_query = self.history[-1][action]
            elif self.current_level == self.F_LIST_FAVORITES:
                self.current_level = self.F_PRODUCT_PAGE
                ret.action = self.F_PRODUCT_PAGE
                ret.id_query = self.history[-1][action]
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
