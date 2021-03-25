from Delivery.Positionable import Positionable


class Warehouse(Positionable):
    def __init__(self, id, position, products):
        super().__init__(position)
        self.id = id
        self.products = products