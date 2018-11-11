#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional


@dataclass
class Params:
    setup_db: bool = False
    update_db: bool = False
    dbname: str = (
        'mysql+mysqlconnector://OCP5:OCP5@localhost/OCP5?charset=utf8mb4'
    )
    search: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    verbose: bool = False
    categories_file: str = 'categories.yml'
    interactive: bool = False
    ui: str = 'console'
