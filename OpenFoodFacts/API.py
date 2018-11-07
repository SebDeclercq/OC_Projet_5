#!/usr/bin/env python3
from OpenFoodFacts.Product import Product
from typing import Dict, Set, Union, Generator, Any, List, NoReturn
import dataclasses
import requests
import re


class API:
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
        self.verbose = verbose

    def _get_products(self,
                     params: Dict[str, Union[int, str]]
                     ) -> Generator[Product, None, None]:
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
            if self._result_complete(result):
                for field in ('categories', 'stores'):
                    result[field] = re.split(
                        r'\s*,\s*', result[field].lower()
                    )
                product: Product = Product(
                    **{k: result[k] for k in self.USEFUL_FIELDS}
                )
                yield product

    def _result_complete(self, result: Dict[str, Union[int, str]]) -> bool:
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
        return self._get_products({
            'tag_0': category,
            'page_size': page_size,
        })
