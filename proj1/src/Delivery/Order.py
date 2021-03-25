from Delivery.ProductContainer import ProductContainer


class Order(ProductContainer):
    def __init__(self, id, position, products):
        super().__init__(position)
        self.id = id
        self._products = products

    def __repr__(self):
        return f"Order(id: {self.id}; position: {self.position}; products: {self._products})"

    def is_complete(self):
        return not self._products
