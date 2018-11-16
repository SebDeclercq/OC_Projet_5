#!/usr/bin/env python3
'''Class representing a minimal Product from OpenFoodFacts API'''
from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    '''Class representing a minimal Product from OpenFoodFacts API'''
    id: int
    name: str
    nutrition_grades: str
    url: str
    stores: List[str]
    categories: List[str]
