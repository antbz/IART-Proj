from typing import Dict, Tuple

from Delivery.Positionable import Positionable
from Delivery.Product import Product

class ProductContainer(Positionable):
    def __init__(self, position: Tuple):
        super().__init__(position)
        self._products : Dict[Product, int] = {}

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