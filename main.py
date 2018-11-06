#!/usr/bin/env python3
from typing import NoReturn, List, Dict, Optional, Any, Generator
import getopt
import sys
from app import App, Params
import os


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
        '   -d --dbname   Database to use (default : sqlite:///:memory:)',
        '   --setup_db    Setup Database (flag)',
        '   -s --search   Keyword to use for simple search',
        '   -c --category Enables category search',
        '   -t --tag      If category search enabled by -c, category to use',
        '   -v --verbose  Display more messages (for dev purpose only)',
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        '   sqlalchemy',
        ''
    )))


def parse_options() -> Params:
    params: Dict[str, Any] = {}
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hd:s:c:t:v', [
                                        'help', 'dbname', 'setup_db',
                                        'search', 'category', 'tag',
                                        'verbose',
                                      ])
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    flags = (option[0] for option in options)
    for option, arg in options:
        if option in ('-d', '--dbname'):
            if 'sqlite:///' in arg and '--setup_db' not in flags:
                dbname: str = arg[arg.find('///') + 3:]
                if not os.path.isfile(dbname) and dbname != ':memory:':
                    print('''SQLite file "%s" doesn't exist''' % dbname)
                    exit()
            params['dbname'] = arg
        elif option == '--setup_db':
            params['setup_db'] = True
        elif option in ('-s', '--search'):
            params['search'] = arg
        elif option in ('-c', '--category'):
            params['category'] = True
        elif option in ('-t', '--tag'):
            params['tag'] = arg
        elif option in ('-h', '--help'):
            usage()
            exit()
        elif option in ('-v', '--verbose'):
            params['verbose'] = True
    return Params(**params)


def main() -> NoReturn:
    params: Params = parse_options()
    app: App = App(params)
    app.run()


if __name__ == '__main__':
    main()
