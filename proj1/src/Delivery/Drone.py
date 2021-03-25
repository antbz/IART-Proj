from typing import Tuple
from Delivery.ProductContainer import ProductContainer


class Drone(ProductContainer):
    def __init__(self, id, max_capacity, position):
        super().__init__(position)
        self.max_capacity = max_capacity
        self.used_capacity = 0
        self.id = id
        self._products = {}

    def set_position(self, position : Tuple):
        self._position = position