from collections import defaultdict
from typing import Dict, List, Tuple

from Delivery.Drone import Drone
from Delivery.Order import Order
from Delivery.Product import Product
from Delivery.Warehouse import Warehouse
from Delivery.Command import Command


class Shipment:
    def __init__(self, drone : Drone, order : Order, warehouse : Warehouse):
        self.drone = drone
        self.order = order
        self.warehouse = warehouse
        self.products : Dict[Product, int] = {}
        self.product_weight = 0
        self.turns = 0
        self.score = 0
        self.percent = 0

        self.fill()

    def __repr__(self):
        return f"Shipment(drone: {self.drone.id}; warehouse: {self.warehouse.id}; order: {self.order.id}; products: {self.products})"
    
    def fill(self):
        prods : List[Tuple[Product, int]] = []
        for product, quantity in self.order.products.items():
            available = min(quantity, self.warehouse.products.get(product, 0))
            if (available  > 0):
                prods.append((product, available))
        
        # TODO improve this, possibly adding knapsack solver

        prods = sorted(prods, key= lambda x : -x[0].weight)
        capacity = self.drone.max_capacity
        carrying : Dict[Product, int] = defaultdict(int)
        for p, q in prods:
            while q > 0:
                if p.weight <= capacity:
                    capacity -= p.weight
                    carrying[p] += 1
                    q -= 1
                else:
                    break
        
        self.products = carrying
        self.product_weight = sum(p.weight * q for p, q in self.products.items())
        self.percent = self.product_weight / self.order.product_weight

        self.calculateScore()

    def calculateScore(self):
        dw = self.drone.distanceTo(self.warehouse)
        do = self.warehouse.distanceTo(self.order)
        self.turns = dw + do + len(self.products) * 2
        self.score = self.percent / self.turns

    def hasProducts(self):
        return len(self.products) > 0
    
    def execute(self):
        self.warehouse.remove_products(self.products)
        self.order.remove_products(self.products)
        self.drone.set_position(self.order.position)
        load, deliver = [], []
        for p, q in self.products.items():
            load.append(Command("L", self.drone, self.warehouse, p, q))
            deliver.append(Command("D", self.drone, self.order, p, q))
        self.drone.commands += load + deliver