#!/usr/bin/env python3
from OpenFoodFacts.API import API
from OpenFoodFacts.Product import Product
from typing import NoReturn, Dict, Any, Generator
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
        '   -d --debug    Enable debug mode',
        '   -s --search   Keyword to use for simple search',
        '   -c --category Enables category search',
        '   -t --tag      If category search enabled by -c, category to use',
        '\nREQUIREMENTS:',
        '   python 3.7+',
        '   requests',
        ''
    )))


def parse_options() -> Dict[str, Any]:
    params: Dict[str, Any] = {
        'debug': False,
        'search': None,
        'tag': None,
    }
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hds:ct:', [
                                        'help', 'debug', 'search',
                                        'category', 'tag'
                                      ])
    except getopt.GetoptError as err:
        print('\033[1mSome error occurred : "%s"\033[0m' % str(err))
        usage()
        exit()
    for option, arg in options:
        if option in ('-d', '--debug'):
            params['debug'] = True
        elif option in ('-s', '--search'):
            params['search'] = arg
        elif option in ('-c', '--category'):
            params['category'] = True
        elif option in ('-t', '--tag'):
            params['tag'] = arg
        elif option in ('-h', '--help'):
            usage()
            exit()
    return params


def simple_search(terms: str) -> Generator[Product, None, None]:
    return API.get_products({
        'search_terms': terms,
    })


def search_by_category(category: str) -> Generator[Product, None, None]:
    return API.get_products({
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
        'tag_0': category
    })


def main() -> NoReturn:
    params: Dict[str, Any] = parse_options()
    API.DEBUG = params['debug']
    if params['search'] is not None:
        products = simple_search(params['search'])
    elif params['tag'] is not None:
        if 'category' in params:
            products = search_by_category(params['tag'])
        ...
    else:
        usage()
        exit()
    for product in products:
        print(product)


if __name__ == '__main__':
    main()
