from delivery.obj import Obj


class Product(Obj):
    def __init__(self, id, weight):
        super().__init__(id)
        self.weight = weight

    def __repr__(self):
        return f"Product(id: {self.id}; weight: {self.weight})"
