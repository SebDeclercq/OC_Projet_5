#!/usr/bin/env python3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sys

if len(sys.argv) > 1:
    dbname = sys.argv[1]
else:
    print('Missing dbname')
    exit()


Base = automap_base()
engine = create_engine('sqlite:///' + dbname)
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
session: Session = Session(engine)

r = session.query(Base.classes.Store)
for store in r:
    for product in store.product_collection:
        print('%s is sold at %s' % (product.name, store.name))

r = session.query(Base.classes.Product)
for product in r:
    for store in product.store_collection:
        print('%s is sold at %s' % (product.name, store.name))
