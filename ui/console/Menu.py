#!/usr/bin/env python3
'''Classes describing menus in the ConsoleUI'''
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Callable, Union, Any


@dataclass
class MenuEntry:
    '''A simple entry in the menu available entry

    Attributes:
        id: Id for the menu entry (1 to 3 characters)
        label: Text to display for the entry
        handler: Callback action to run if entry is selected
        args: Optional arguments for the handler'''
    id: str
    label: str
    handler: Callable
    args: Any

    def __repr__(self) -> str:
        '''Formatted printing Menu Entry'''
        return f'{self.id:3} - {self.label}'


@dataclass
class Menu:
    '''A menu in the ConsoleUI

    Attributes:
        counter: Used to increment ids in the MenuEntry if not provided
        entries: List of the available MenuEntries'''
    counter: int = 1
    entries: Dict[str, MenuEntry] = field(default_factory=dict)

    def add(self, label: str, handler: Callable,
            id: Optional[Union[int, str]] = None,
            args: Any = None) -> None:
        '''Method adding a new MenuEntry to the Menu'''
        if not id and id != 0:
            id = self.counter
            self.counter += 1
        self.entries[str(id)] = MenuEntry(str(id), label, handler, args)
