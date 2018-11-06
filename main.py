#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
from sqlalchemy.orm import Session
import db.setup
from db import Base
import getopt
import sys


def usage() -> NoReturn:
    print('\n'.join((
        '\nDESCRIPTION: ',
        'This main script is intended to pilot all processing actions for ',
        'the P5 of OpenClassRooms DA Python. It currently creates the ',
        'database if the correponding options are provided.',
        '\nUSAGE: ',
        '   python app.py [OPTIONS]',
        '\nOPTIONS:',
        '   -h --help     Display this help guide',
        '   -d --dbname   Database to use (default : sqlite:///:memory:)'
        '   --setup_db    Setup Database (flag)'
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        '   sqlalchemy',
        ''
    )))


def parse_options() -> Dict[str, Any]:
    params: Dict[str, Any] = {
        'dbname': 'sqlite:///:memory:',
        'setup_db': False
    }
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hd:', [
                                        'help', 'dbname', 'setup_db'
                                      ])
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    for option, arg in options:
        if option in ('-d', '--dbname'):
            params['dbname'] = arg
        elif option == '--setup_db':
            params['setup_db'] = True
        elif option in ('-h', '--help'):
            usage()
            exit()
    return params


def main() -> NoReturn:
    params = parse_options()
    if params['setup_db'] or params['dbname'] == 'sqlite:///:memory:':
        db.setup.start_up(params['dbname'])
    else:
        session: Session = db.connect(params['dbname'])


if __name__ == '__main__':
    main()
