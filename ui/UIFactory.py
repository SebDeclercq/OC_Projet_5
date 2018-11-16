#!/usr/bin/env python3
'''Factory class used to dynamically instanciated the asked UI.
Currently, handles a ConsoleUI only'''
from .console import ConsoleUI
from .UI import UI


class UIFactory:
    '''Factory class used to dynamically instanciated the asked UI.'''
    @staticmethod
    def factory(type: str) -> UI:
        '''Static method instanciated a UI based on the type parameter
        and returns it'''
        type = type.lower()
        if type == 'console':
            ui = ConsoleUI()
        else:
            raise ValueError('Unkown type "%s" for UIs' % type)
        if not isinstance(ui, UI):
            raise TypeError('UI "%s" does\'nt implement UI "interface"' % type)
        else:
            return ui
