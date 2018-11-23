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

    @abstractmethod
    def start(self, app: App) -> None:
        '''Abstract method forcing every child to implement
        an interaction between the App and the user'''
        pass
