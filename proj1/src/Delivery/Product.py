class Product:
    def __init__(self, id, weight):
        self.weight = weight
        self.id = id

    def __repr__(self):
        return f"Product(id: {self.id}; weight: {self.weight})"
