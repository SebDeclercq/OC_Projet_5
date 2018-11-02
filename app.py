#!/usr/bin/env python3
from OpenFoodFacts.API import API
from typing import NoReturn, Dict, Any
import getopt
import sys


def parse_options() -> Dict[str, Any]:
    params: Dict[str, Any] = {'debug': False}
    options, args = getopt.getopt(sys.argv[1:], 'd', ['debug'])
    for option, arg in options:
        if option in ('-d', '--debug'):
            params['debug'] = True
    return params


def main() -> NoReturn:
    params: Dict[str, Any] = parse_options()
    API.DEBUG = params['debug']
    products = API.get_products({
        'search_terms': 'chocolats+noirs',
    })
    for product in products:
        print(product)


if __name__ == '__main__':
    main()
