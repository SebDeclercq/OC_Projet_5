#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Product:
    product_name: str
    brands: str
    nutrition_grades: str
    url: str
    stores: str
    categories: str
