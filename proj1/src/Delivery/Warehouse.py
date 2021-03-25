from Delivery.ProductContainer import ProductContainer


class Warehouse(ProductContainer):
    def __init__(self, id, position, products):
        super().__init__(position)
        self.id = id
        self._products = products

    def __repr__(self):
        return f"Warehouse(id: {self.id}; products: {self.products})"