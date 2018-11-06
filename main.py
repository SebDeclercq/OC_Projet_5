#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import getopt
import sys
from app import App, Params


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


def parse_options() -> Params:
    params: Dict[str, Any] = {}
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
    return Params(**params)


def main() -> NoReturn:
    params: Params = parse_options()
    app: App = App(params)
    app.run()


if __name__ == '__main__':
    main()
