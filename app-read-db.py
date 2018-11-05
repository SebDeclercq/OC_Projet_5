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
r = session.query(Base.classes.Product)
for p in r:
    print(p.__dict__)
