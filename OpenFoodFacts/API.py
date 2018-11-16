#!/usr/bin/env python3
'''Class interfacing the App and the OpenFoodFacts's API'''
from OpenFoodFacts.Product import Product
from typing import Dict, Set, Union, Generator, Any, List, NoReturn
import dataclasses
import requests
import re


class API:
    '''Class interfacing the App and the OpenFoodFacts's API

    Class attributes:
        BASE_URL:      URL to the API without parameter
        BASE_PARAMS:   Dictionary containing base parameters for the API
        USEFUL_FIELDS: Collects dynamically the Product attributes names.
                       Simplifies the collection of the wanted data only.'''
    BASE_URL: str = 'https://fr.openfoodfacts.org/cgi/search.pl'
    BASE_PARAMS: Dict[str, Union[int, str]] = {
        'action': 'process',
        'page_size': 20,
        'json': 1,
        'sort_by': 'unique_scans_n',
        'tagtype_0': 'categories',
        'tag_contains_0': 'contains',
    }
    USEFUL_FIELDS: Set[str] = {
        field.name for field in dataclasses.fields(Product)
    }

    def __init__(self, verbose: bool = False) -> None:
        '''Constructor'''
        self.verbose = verbose

    def _get_products(self,
                      params: Dict[str, Union[int, str]]
                      ) -> Generator[Product, None, None]:
        '''Private method calling the API with the parameters provided.
        Instanciates a Product object for every products collected in
        the API response and yields them'''
        r_params: Dict[str, Union[int, str]] = self.BASE_PARAMS.copy()
        r_params.update(params)
        r_result: requests.Response = requests.get(self.BASE_URL, r_params)
        if self.verbose:
            print(r_result.url)
        if r_result.status_code != requests.codes.ok:
            r_result.raise_for_status()
        products: List[Dict[str, Any]] = r_result.json()['products']
        for result in products:
            result['name'] = result.pop('product_name')
            if self._result_complete(result):  # If all data are available
                for field in ('categories', 'stores'):
                    result[field] = re.split(
                        r'\s*,\s*', result[field].lower()
                    )
                product: Product = Product(
                    **{k: result[k] for k in self.USEFUL_FIELDS}
                )
                yield product

    def _result_complete(self, result: Dict[str, Union[int, str]]) -> bool:
        '''Private method that checks if the collected metadata from the
        API contains every required elements (returns True/False)'''
        for field in self.USEFUL_FIELDS:
            if field not in result or not result[field]:
                if self.verbose:
                    print(
                        'Missing field "%s" for product %s'
                        % (field, result['code'])
                    )
                return False
        return True

    def search(self, category: str,
               page_size: int = 20) -> Generator[Product, None, None]:
        '''Public method to query the API based on
        a category id. Yields associated Products'''
        return self._get_products({
            'tag_0': category,
            'page_size': page_size,
        })
