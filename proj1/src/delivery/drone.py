from typing import Tuple

from delivery.product_container import ProductContainer


class Drone(ProductContainer):
    def __init__(self, id, max_capacity, max_turns, position):
        super().__init__(id, position)
        self.max_capacity = max_capacity
        self.max_turns = max_turns
        self.turn = 0

    def __repr__(self):
        return f"Drone(id: {self.id}; position: {self.position}; max_capacity: {self.max_capacity}; products: {self.products}"

    def set_position(self, position: Tuple):
        self.position = position

    def add_turns(self, turns):
        self.turn += turns
