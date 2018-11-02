#!/usr/bin/env python3
from OpenFoodFacts.Product import Product
from typing import Dict, Set, Union, Generator, Any, List
import dataclasses
import requests


class API:
    DEBUG: bool = False
    BASE_URL: str = 'https://fr.openfoodfacts.org/cgi/search.pl'
    BASE_PARAMS: Dict[str, Union[int, str]] = {
        'action': 'process',
        'page_size': 20,
        'json': 1,
        'sort_by': 'unique_scans_n',
    }
    USEFUL_FIELDS: Set[str] = {
        field.name for field in dataclasses.fields(Product)
    }

    @classmethod
    def get_products(cls,
                     params: Dict[str, Union[int, str]]
                     ) -> Generator:
        r_params: Dict[str, Union[int, str]] = cls.BASE_PARAMS.copy()
        r_params.update(params)
        r_result: requests.Response = requests.get(cls.BASE_URL, r_params)
        if cls.DEBUG:
            print(r_result.url)
        if r_result.status_code != requests.codes.ok:
            r_result.raise_for_status()
        products: List[Dict[str, Any]] = r_result.json()['products']
        for result in products:
            if cls._result_complete(result):
                product: Product = Product(
                    **{k: result[k] for k in cls.USEFUL_FIELDS}
                )
                yield product

    @classmethod
    def _result_complete(cls, result: Dict[str, Union[int, str]]) -> bool:
        for field in cls.USEFUL_FIELDS:
            if field not in result or not result[field]:
                if cls.DEBUG:
                    print(
                        'Missing field "%s" for product %s'
                        % (field, result['code'])
                    )
                return False
        return True
