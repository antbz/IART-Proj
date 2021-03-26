from Delivery.Drone import Drone
from Delivery.Product import Product
from Delivery.ProductContainer import ProductContainer


class Command:
    def __init__(self, type : str, drone : Drone, destination : ProductContainer, product : Product, quantity : int):
        self.type = type
        self.drone = drone
        self.destination = destination
        self.product = product
        self.quantity = quantity
    
    @property
    def command_str(self):
        return f"{self.drone.id} {self.type} {self.destination.id} {self.product.id} {self.quantity}"