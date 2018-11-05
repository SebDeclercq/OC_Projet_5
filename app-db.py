#!/usr/bin/env python3
import db
from typing import NoReturn
import sys

def main() -> NoReturn:
    if len(sys.argv) > 1:
        dbname = sys.argv[1]
    else:
        dbname = ':memory:'
    db.start_up(dbname)


if __name__ == '__main__':
    main()
