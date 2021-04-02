from typing import Dict, Tuple

from delivery.positionable import Positionable
from delivery.product import Product


class ProductContainer(Positionable):
    def __init__(self, id, position: Tuple):
        super().__init__(id, position)
        self._products: Dict[Product, int] = {}

    @property
    def products(self):
        return self._products

    @property
    def product_weight(self):
        return sum(p.weight * q for p, q in self._products.items())

    def add_products(self, products: Dict[Product, int]):
        for product, quantity in products.items():
            if product in self._products:
                self._products[product] += quantity
            else:
                self._products[product] = quantity

    def remove_products(self, products: Dict[Product, int]):
        for product, quantity in products.items():
            self._products[product] -= quantity
            if self._products[product] == 0:
                self._products.pop(product)

    def remove_all_products(self):
        self._products = {}

    def has_all_products(self, products: Dict[Product, int]):
        for product, quantity in products.items():
            own = self._products.get(product)
            if own == None or own < quantity:
                return False
        return True
