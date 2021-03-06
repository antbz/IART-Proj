from delivery.product_container import ProductContainer


class Warehouse(ProductContainer):
    def __init__(self, id, position, products):
        super().__init__(id, position)
        self._products = products

    def __repr__(self):
        return f"Warehouse(id: {self.id}; position: {self.position}; products: {self.products})"
