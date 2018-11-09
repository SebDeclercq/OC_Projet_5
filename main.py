#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import getopt
import sys
from app import App, Params
import os


def usage() -> None:
    print('\n'.join((
        '\nDESCRIPTION: ',
        'This main script is intended to pilot all processing actions for ',
        'the P5 of OpenClassRooms DA Python. It currently creates the ',
        'database or updates it if the correponding options are provided.',
        '\nUSAGE: ',
        '   python app.py [OPTIONS]',
        '\nOPTIONS:',
        '   -h --help        Displays this help guide',
        '   -d --dbname      Database to use (default : sqlite:///:memory:)',
        '   --setup_db       Sets up database (flag)',
        '   -u --update_db   Updates database content (flag)',
        '   --categories     File containing the wished categories in database',
        '   -i --interactive Active interactive mode (flag)',
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        '   sqlalchemy',
        '   pyyaml'
        ''
    )))


def parse_options() -> Params:
    params: Dict[str, Any] = {}
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hd:vui', [
                                        'help', 'dbname', 'setup_db',
                                        'verbose', 'update_db', 'categories',
                                        'interactive',
                                      ])
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    flags = (option[0] for option in options)
    for option, arg in options:
        if option in ('-d', '--dbname'):
            params['dbname'] = arg
        elif option == '--setup_db':
            params['setup_db'] = True
        elif option in ('-u', '--update_db'):
            params['update_db'] = True
        elif option == 'categories':
            params['categories_file'] = arg
        elif option in ('-i', '--interactive'):
            params['interactive'] = True
        elif option in ('-h', '--help'):
            usage()
            exit()
        elif option in ('-v', '--verbose'):
            params['verbose'] = True
    return Params(**params)


def main() -> None:
    params: Params = parse_options()
    app: App = App(params)
    try:
        app.run()
    except Exception as err:
        print(err)
        exit()


if __name__ == '__main__':
    main()
