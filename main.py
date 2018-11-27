#!/usr/bin/env python3
'''Main script starting up this OC P5 program.
This script is parametrized with CLI options, which are described
with a usage() function available with pipenv run python main.py --help.
Please refer to this help guide for further information.'''

from typing import NoReturn, List, Dict, Optional, Any, Generator
import getopt
import sys
import os
from app import App, Params


def usage() -> None:
    '''function acting as "Help guide"'''
    print('\n'.join((
        '\nDESCRIPTION: ',
        'This main script is intended to pilot all processing actions for ',
        'the P5 of OpenClassRooms DA Python. It creates the database or ',
        'updates it if the correponding options are provided. Its main ',
        'goals are to interact with collected OpenFoodFacts data in order ',
        'to select healthier products than your regular.',
        '\nUSAGE: ',
        '   python main.py [OPTIONS]',
        '\nMODES:',
        '   --setup_db       Sets up database (flag)',
        '   --update_db      Updates database content (flag)',
        '   -i --interactive DEFAULT: Active interactive mode (flag)',
        '\nOPTIONS:',
        '   --categories File containing the wished categories in database',
        '   -u --user    Username for MySQL database (useless for SQLite)',
        '   -p --pass    Password for MySQL database (useless for SQLite)',
        '   -d --dbname  Database to use (for SQLite: "sqlite:///[DBNAME]")',
        '',
        '   -h --help    Displays this help guide',
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        '   sqlalchemy',
        '   pyyaml',
        '   mysql-connector-python',
        ''
    )))


def parse_options() -> Params:
    '''Function parsing CLI commands with getopt.
    It creates a Params object and returns it.'''
    params: Dict[str, Any] = {}
    try:
        options, args = getopt.getopt(
            sys.argv[1:], 'ic:u:p:d:h', [
                'setup_db', 'update_db', 'interactive',
                'categories', 'user', 'pass', 'dbname',
                'help'
            ]
        )
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    modes = []
    for option, arg in options:
        # MODES
        if option == '--setup_db':
            params['setup_db'] = True
            modes.append('setup_db')
        elif option == '--update_db':
            params['update_db'] = True
            modes.append('update_db')
        elif option in ('-i', '--interactive'):
            params['interactive'] = True
            modes.append('interactive')
        # OPTIONS
        elif option in ('-u', '--user'):
            params['user'] = arg
        elif option in ('-p', '--pass'):
            params['password'] = arg
        elif option in ('-d', '--dbname'):
            params['dbname'] = arg
        elif option == 'categories':
            params['categories_file'] = arg
        elif option in ('-h', '--help'):
            usage()
            exit()
    if len(modes) != 1:  # If more (or no) modes selected
        for mode in modes:
            params[mode] = False
        params['interactive'] = True  # Use interactive as default
    return Params(**params)


def main() -> None:
    '''Main function'''
    params: Params = parse_options()
    app: App = App(params)
    try:
        app.run()
    except Exception as err:
        print(err)
        exit()


if __name__ == '__main__':
    main()
