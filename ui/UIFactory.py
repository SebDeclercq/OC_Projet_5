#!/usr/bin/env python3
from .console import ConsoleUI
from .UI import UI


class UIFactory:
    @staticmethod
    def factory(type: str) -> UI:
        type = type.lower()
        if type == 'console':
            ui = ConsoleUI()
        else:
            raise ValueError('Unkown type "%s" for UIs' % type)
        if not isinstance(ui, UI):
            raise TypeError('UI "%s" does\'nt implement UI "interface"' % type)
        else:
            return ui
