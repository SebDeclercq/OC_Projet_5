#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    product_name: str
    brands: str
    nutrition_grades: str
    url: str
    stores: List[str]
    categories: List[str]
