#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
from sqlalchemy.orm import Session
import db.setup
from db import Base
from app import Params


class App:
    session: Session
    params: Params

    def __init__(self, params: Params) -> NoReturn:
        self.params = params

    def run(self) -> NoReturn:
        if self.params.setup_db or self.params.dbname == 'sqlite:///:memory:':
            self.session = db.setup.start_up(self.params.dbname)
        else:
            self.session = db.connect(self.params.dbname)
