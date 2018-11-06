#!/usr/bin/env python3
import db.setup
from typing import NoReturn
import sys
from sqlalchemy.orm import session, query


def populate(session: session.Session) -> NoReturn:
    store: db.setup.Store = db.setup.Store(name='vival')
    session.add(store)
    product: db.setup.Product = db.setup.Product(
        id=123, name='chips casino', nutrition_grade='E',
        url='http://vival/chips%20casino', stores=[store]
    )
    session.add(product)
    product = db.setup.Product(
        id=456, name='perrier', nutrition_grade='A',
        url='http://vival/perrier', stores=[store]
    )
    session.add(product)
    session.commit()


def scan(session: session.Session) -> NoReturn:
    r: query.Query = session.query(db.setup.Store)
    for store in r:
        for product in store.products:
            print('%s is sold at %s' % (product.name, store.name))
    r = session.query(db.setup.Product)
    for product in r:
        for store in product.stores:
            print('%s is sold at %s' % (product.name, store.name))


def main() -> NoReturn:
    if len(sys.argv) > 1:
        dbname = sys.argv[1]
    else:
        dbname = ':memory:'
    session = db.setup.start_up(dbname)
    populate(session)
    scan(session)


if __name__ == '__main__':
    main()
