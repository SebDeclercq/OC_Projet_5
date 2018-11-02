#!/usr/bin/env python3
from OpenFoodFacts.API import API
from typing import NoReturn, Dict, Any
import getopt
import sys


def usage() -> NoReturn:
    print('\n'.join((
        '\nDESCRIPTION: ',
        'This script is meant to have a straight forward interface '
        'to the OpenFoodFacts API.',
        'It is intended to evolve.',
        '\nUSAGE: ',
        '   python app.py [OPTIONS]',
        '\nOPTIONS:',
        '   -h --help     Display this help guide',
        '   -t --terms    Terms to use for requesting OpenFoodFacts API',
        '   -d --debug    Enable debug mode',
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        ''
    )))


def parse_options() -> Dict[str, Any]:
    params: Dict[str, Any] = {
        'debug': False,
        'terms': None
    }
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hdt:',
                                      ['help', 'debug', 'terms'])
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    for option, arg in options:
        if option in ('-d', '--debug'):
            params['debug'] = True
        elif option in ('-t', '--terms'):
            params['terms'] = arg
        elif option in ('-h', '--help'):
            usage()
            exit()
    return params


def main() -> NoReturn:
    params: Dict[str, Any] = parse_options()
    API.DEBUG = params['debug']
    if params['terms'] is not None:
        products = API.get_products({
            'search_terms': params['terms'],
        })
    else:
        usage()
        exit()
    for product in products:
        print(product)


if __name__ == '__main__':
    main()
