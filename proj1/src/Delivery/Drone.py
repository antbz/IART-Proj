from typing import Tuple

from Delivery.ProductContainer import ProductContainer


class Drone(ProductContainer):
    def __init__(self, id, max_capacity, max_turns, position):
        super().__init__(id, position)
        self.max_capacity = max_capacity
        self.max_turns = max_turns
        self.used_capacity = 0
        self.turn = 0

    def __repr__(self):
        return f"Drone(id: {self.id}; position: {self.position}; max_capacity: {self.max_capacity}; products: {self.products} shipments: {self.shipments}); "

    def set_position(self, position: Tuple):
        self.position = position

    def add_turns(self, turns):
        self.turn += turns
