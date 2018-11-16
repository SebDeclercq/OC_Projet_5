#!/usr/bin/env python3
'''UI in console'''
from typing import NoReturn, List, Dict, Optional, Any, Union, Callable
import yaml
import os
import platform
from ..UI import UI
from ..UIReturn import UIReturn
from db import DBProduct, DBCategory


class ConsoleUI(UI):
    '''Class describing the UI in console.
    Inherits from the UI abstract class

    Attributes:
        error: True if an error has occurred
        current_level: Describes where we currently are
        page_content: Holds the text to display page by page
        list_menus: List of the menu-like pages
        product_pages: List of a product details pages
        history: Holds the previous actions
        data: Holds the provided data by the App (if any)'''

    def __init__(self) -> None:
        '''Constructor'''
        self.error: bool = False
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
        self.data: Any = None
        text_file: str = os.path.join('ui', 'console', 'page_contents.yml')
        with open(text_file, encoding='utf-8') as f:  # Get page contents
            text: Dict[str, str] = yaml.load(f)
        for page_name, page_content in text.items():
            page_level = getattr(self, page_name)
            self.page_contents[page_level] = page_content.rstrip()

    def display(self, data: Any = None) -> Any:
        '''Method rendering actions to the user in the console'''
        # self._clear_screen()  # Screen gets the hiccups with that command...
        if self.error:
            data = self.data
            self.error = False
            self.data = None
            if self.history:
                self.history.pop()
        if self.current_level == self.WELCOME:
            # If we're at the top page for the first time
            print(self.page_contents[self.WELCOME])
            self.current_level = self.TOP_MENU
        if self.current_level not in self.product_pages:
            # If we're on a list-like page, simply renders text
            print(self.page_contents[self.current_level])
        if data:  # If the App has provided data
            self.data = data
            if self.current_level in self.list_menus:
                # If we're on a list-like page, adds a line by item
                # and saves the pair action/code in the history attribute
                actions: Dict[int, int] = {}
                for idx, element in enumerate(data):
                    no_el: int = idx + 1
                    if self.current_level == self.S_LIST_CATEGO:
                        print('%-3s - %s' % (str(no_el),
                                             element.name.capitalize()))
                    else:
                        print('%-3s - (NUTRISCORE: %s) %s' % (
                            str(no_el),
                            element.nutrition_grade.upper(),
                            element.name.capitalize()
                        ))
                    actions[no_el] = element.id
                self.history.append(actions)
            elif self.current_level in self.product_pages:
                # If we're on a product details page, shows text
                # with metadata and add the product's id
                # to the history attribute
                print(self.page_contents[self.current_level] % data)
                if 'id' in data:
                    self.history.append(data['id'])
        else:  # If no data provided
            if self.current_level in self.list_menus:
                # If we're on a list-like page, prints message
                print('\nAucun résultat trouvé\n')
        if self.current_level != self.TOP_MENU:
            # For every page except top, add a 0 option to go back to the top
            print("0   - Retour à l'accueil")
        print("q   - Quitter")  # Add a q "quit" option to every page

    def interact(self) -> UIReturn:
        '''Method interacting with the user in the console.
        Generates a UIReturn object based on the user's actions
        and returns it to the App.'''
        ret: UIReturn = UIReturn()
        command: str = input('> ').lower()
        if command in ('q', 'quit', 'e', 'exit'):
            ret.message = 'Bye !'
            ret.action = self.QUIT
        else:
            if not command.isdigit():
                ret.message = self._error(command)
                return ret
            else:  # If an real action occurred
                action: int = int(command)  # Get the action's code
            if action == self.GO_BACK_TO_TOP_MENU:
                self.current_level = self.WELCOME
                self.history = []  # Clear history every time you meet the top
            elif self.current_level == self.TOP_MENU:
                # If we're at the top
                if action == 1:
                    # Displays categories and updates level
                    self.current_level = self.S_LIST_CATEGO
                    ret.action = self.S_LIST_CATEGO
                elif action == 2:
                    # Displays favorites and updates level
                    self.current_level = self.F_LIST_FAVORITES
                    ret.action = self.F_LIST_FAVORITES
                else:  # Unknown
                    ret.message = self._error(action)
            elif self.current_level == self.S_LIST_CATEGO:
                # If we're on the categories-list page
                if action in self.history[-1]:
                    # While an action-id is entered, collects
                    # the corresponding action in the history,
                    # updates the level and returns the action
                    self.current_level = self.S_LIST_PRODUCTS
                    ret.action = self.S_LIST_PRODUCTS
                    ret.id_query = self.history[-1][action]
                else:  # Unknown
                    ret.message = self._error(action)
            elif self.current_level == self.S_LIST_PRODUCTS:
                # If we're on the products-list page
                if action in self.history[-1]:
                    # While an action-id is entered, collects
                    # the corresponding action in the history,
                    # updates the level and returns the action
                    self.current_level = self.S_PRODUCT_PAGE
                    ret.action = self.S_PRODUCT_PAGE
                    ret.id_query = self.history[-1][action]
                else:  # Unknown
                    ret.message = self._error(action)
            elif self.current_level == self.S_PRODUCT_PAGE:
                # If we're on a product page in the substitution part
                if action == 1:  # => "Show substitutes"
                    # Collects the corresponding action in the history,
                    # updates the level and returns the action
                    self.current_level = self.S_LIST_SUBSTITUTES
                    ret.action = self.S_LIST_SUBSTITUTES
                    ret.id_query = self.history[-1]
                elif action == 2:  # => "Save favorite substitution"
                    # Collects the ids for the substituted
                    # and substitute products
                    ret.substitution_ids = []
                    for p_id in (self.history[-3], self.history[-1]):
                        if isinstance(p_id, int):
                            ret.substitution_ids.append(p_id)
                    if len(ret.substitution_ids) != 2:
                        # If no product's been seen before this one,
                        # it is not possible to save anything
                        ret.message = ('Vous ne pouvez pas sauvegarder '
                                       'en favori un produit non substitué')
                        self.error = True
                    else:
                        # If ok, updates the level and returns the action
                        self.current_level = self.S_SAVED_FAVORITE
                        ret.action = self.S_SAVED_FAVORITE
                else:  # Unknown
                    ret.message = self._error(action)
            elif self.current_level == self.S_LIST_SUBSTITUTES:
                # If we're on the substitute-list page
                if action in self.history[-1]:
                    # While an action-id is entered, collects
                    # the corresponding action in the history,
                    # updates the level and returns the action
                    self.current_level = self.S_PRODUCT_PAGE
                    ret.action = self.S_PRODUCT_PAGE
                    ret.id_query = self.history[-1][action]
                else:  # Unknown
                    ret.message = self._error(action)
            elif self.current_level == self.F_LIST_FAVORITES:
                # If we're on the favorites-list page
                if self.history and action in self.history[-1]:
                    # While an action-id is entered, collects
                    # the corresponding action in the history,
                    # updates the level and returns the action
                    self.current_level = self.F_PRODUCT_PAGE
                    ret.action = self.F_PRODUCT_PAGE
                    ret.id_query = self.history[-1][action]
                else:  # Unknown
                    ret.message = self._error(action)
            else:  # Unknown
                ret.message = self._error(action)
        if ret.message:  # bold + highlight red
            ret.message = '\033[1m\033[41m' + ret.message + '\033[0m'
        return ret

    def _error(self, action: Union[str, int]) -> str:
        '''If an error has occurred, pass self.error to True and
        return a message to print in the UI'''
        self.error = True
        message: str = 'Action %s inconnue' % action
        message += '\nVeuillez saisir un chiffre présent dans le menu'
        return message

    def _clear_screen(self) -> None:
        '''Unused method because the screen gets the hiccups
        with that command... But it'd be cool if not'''
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
