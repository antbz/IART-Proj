from Delivery.Positionable import Positionable


class Drone(Positionable):
    def __init__(self, id, max_capacity, position):
        super().__init__(position)
        self.max_capacity = max_capacity
        self.used_capacity = 0
        self.id = id
        self.products = {}