#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Callable, Union, Any


@dataclass
class MenuEntry:
    id: str
    label: str
    handler: Callable
    args: Any
    menu: Menu

    def __repr__(self) -> str:
        return f'{self.id:3} - {self.label}'


@dataclass
class Menu:
    counter: int = 1
    entries: Dict[str, MenuEntry] = field(default_factory=dict)

    def add(self, label: str, handler: Callable,
            id: Optional[Union[int, str]] = None,
            args: Any = None) -> None:
        if not id and id != 0:
            id = self.counter
            self.counter += 1
        self.entries[str(id)] = MenuEntry(str(id), label, handler, args, self)
