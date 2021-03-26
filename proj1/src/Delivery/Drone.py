from typing import List, Tuple

from Delivery.ProductContainer import ProductContainer


class Drone(ProductContainer):
    def __init__(self, id, max_capacity, position):
        super().__init__(id, position)
        self.max_capacity = max_capacity
        self.used_capacity = 0
        self.commands = []

    def __repr__(self):
        return f"Drone(id: {self.id}; position: {self.position}; max_capacity: {self.max_capacity}; products: {self.products}) "

    def set_position(self, position: Tuple):
        self.position = position

    def add_command(self, command):
        self.commands.append(command)