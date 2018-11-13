#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


@dataclass
class Params:
    setup_db: bool = False
    update_db: bool = False
    user: str = 'OCP5'
    password: str = 'OCP5'
    dbname: str = 'OCP5'
    search: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    verbose: bool = False
    categories_file: str = 'categories.yml'
    interactive: bool = False
    ui: str = 'console'

    @property
    def db_uri(self) -> str:
        if 'sqlite' in self.dbname:
            return self.dbname
        else:
            return (
                'mysql+mysqlconnector://%s:%s@localhost/%s?charset=utf8mb4'
                % (self.user, self.password, self.dbname)
            )
