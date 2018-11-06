#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Params:
    setup_db: bool = False
    dbname: str = 'sqlite:///:memory:'
