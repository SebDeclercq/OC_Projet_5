#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Optional, Any


class UI(ABC):
    WELCOME: int = 1
    TOP_MENU: int = 2
    GO_BACK_TO_TOP_MENU: int = 0
    S_LIST_CATEGO: int = 3  # S_ for "substitute"
    S_LIST_PRODUCTS: int = 4
    S_PRODUCT_PAGE: int = 5
    F_LIST_FAVORITES: int = 6  # F_ for "favorite"
    F_PRODUCT_PAGE: int = 7
    S_LIST_SUBSTITUTES: int = 8
    QUIT: int = -1

    @abstractmethod
    def interact(self) -> Any:
        pass

    @abstractmethod
    def display(self, data: Optional[Any] = None) -> Any:
        pass
