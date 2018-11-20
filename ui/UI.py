#!/usr/bin/env python3
'''Abstract class which will be the parent class of all the UIs.
Forces all children to have an interact() method and a display() method
and shares class variables too.'''
from abc import ABC, abstractmethod
from app import App


class UI(ABC):
    '''Abstract class which will be the parent class of all the UIs.
    Forces all children to have an interact() method and a display() method
    and shares class variables too.'''
    WELCOME: int = 1
    TOP_MENU: int = 2
    GO_BACK_TO_TOP_MENU: int = 0
    S_LIST_CATEGO: int = 3  # S_ for "substitute"
    S_LIST_PRODUCTS: int = 4
    S_PRODUCT_PAGE: int = 5
    F_LIST_FAVORITES: int = 6  # F_ for "favorite"
    F_PRODUCT_PAGE: int = 7
    S_LIST_SUBSTITUTES: int = 8
    S_SAVED_FAVORITE: int = 9
    QUIT: int = -1

    @abstractmethod
    def start(self, app: App) -> None:
        '''Abstract method forcing every child to implement
        an interaction between the App and the user'''
        pass
