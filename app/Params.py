#!/usr/bin/env python3
'''"Container"-like class meant to hold all parameters for the App'''

from dataclasses import dataclass
from typing import Optional


@dataclass
class Params:
    '''"Container"-like class meant to hold all parameters for the App'''
    setup_db: bool = False
    update_db: bool = False
    user: str = 'OCP5'
    password: str = 'OCP5'
    dbname: str = 'OCP5'
    search: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    categories_file: str = 'categories.yml'
    interactive: bool = False
    ui: str = 'console'

    @property
    def db_uri(self) -> str:
        '''Property method returning the database URI.
        Creates dynamically the MySQL URI.'''
        if 'sqlite' in self.dbname:
            return self.dbname
        else:
            return (
                'mysql+mysqlconnector://%s:%s@localhost/%s?charset=utf8mb4'
                % (self.user, self.password, self.dbname)
            )
