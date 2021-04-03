from collections import defaultdict
from typing import Dict, List, Tuple

from ortools.algorithms import pywrapknapsack_solver

from delivery.command import Command
from delivery.drone import Drone
from delivery.order import Order
from delivery.product import Product
from delivery.warehouse import Warehouse


class Shipment:
    def __init__(self, drone, order, warehouse, products, product_weight, turns, score, percent) -> None:
        self.drone: Drone = drone
        self.order: Order = order
        self.warehouse: Warehouse = warehouse
        self.products: Dict[Product, int] = products
        self.product_weight = product_weight
        self.turns = turns
        self.score = score
        self.percent = percent
        self.is_active: bool = True

    def __repr__(self):
        return f"Shipment(active: {self.is_active}; drone: {self.drone.id}; warehouse: {self.warehouse.id}; order: {self.order.id}; products: {self.products})"

    @classmethod
    def fromcommands(cls, commands: List[Command]):
        drone = commands[0].drone
        order = commands[-1].destination
        wh = commands[0].destination
        products = {}
        for cmd in commands:
            if cmd.type == 'D':
                break
            products.update({cmd.product: cmd.quantity})

        sh = cls(drone, order, wh, products, 0, 0, 0, 0)
        sh.calculateScore()
        return sh

    @classmethod
    def fromdow(cls, drone: Drone, order: Order, warehouse: Warehouse):
        sh = cls(drone, order, warehouse, {}, 0, 0, 0, 0)
        sh.fill()
        return sh

    @property
    def commands(self):
        load, deliver = [], []
        for p, q in self.products.items():
            load.append(Command("L", self.drone, self.warehouse, p, q))
            deliver.append(Command("D", self.drone, self.order, p, q))
        return load + deliver

    def fill(self):
        prods: List[Tuple[Product, int]] = []
        for product, quantity in self.order.products.items():
            available = min(quantity, self.warehouse.products.get(product, 0))
            if (available > 0):
                prods.append((product, available))

        prods = sorted(prods, key=lambda x: -x[0].weight)
        capacity = self.drone.max_capacity
        carrying: Dict[Product, int] = defaultdict(int)
        for p, q in prods:
            while q > 0:
                if p.weight <= capacity:
                    capacity -= p.weight
                    carrying[p] += 1
                    q -= 1
                else:
                    break

        self.products = carrying

        self.calculateScore()

    def knapsack(self):
        prods = []
        values = []
        weights = [[]]
        capacity = [self.drone.max_capacity]

        for product, quantity in self.order.products.items():
            available = min(quantity, self.warehouse.products.get(product, 0))
            for q in range(available):
                prods.append(product)
                values.append(product.weight)
                weights[0].append(product.weight)

        solver = pywrapknapsack_solver.KnapsackSolver(
            pywrapknapsack_solver.KnapsackSolver.
                KNAPSACK_64ITEMS_SOLVER, 'KnapsackExample')

        solver.Init(values, weights, capacity)
        solver.Solve()

        total_weight = 0
        carrying: Dict[Product, int] = defaultdict(int)

        for i in range(len(values)):
            if solver.BestSolutionContains(i):
                product = prods[i]
                if carrying.__contains__(product):
                    carrying[product] += 1
                else:
                    carrying[product] = 1
                total_weight += weights[0][i]

        self.products = carrying
        self.percent = total_weight / self.order.product_weight

        self.calculateScore()

    def calculateScore(self):
        self.product_weight = sum(p.weight * q for p, q in self.products.items())
        self.percent = self.product_weight / self.order.product_weight
        self.calculate_turns()
        self.score = self.percent / self.turns

    def calculate_turns(self):
        dw = self.drone.distanceTo(self.warehouse)
        do = self.warehouse.distanceTo(self.order)
        self.turns = dw + do + len(self.products) * 2

    def hasProducts(self):
        return len(self.products) > 0

    def execute(self):
        if not (self.warehouse.has_all_products(self.products) and
                self.order.has_all_products(self.products) and
                self.drone.turn + self.turns <= self.drone.max_turns):
            return False
        self.warehouse.remove_products(self.products)
        self.order.remove_products(self.products)
        self.drone.set_position(self.order.position)
        self.drone.add_turns(self.turns)
        self.order.add_delivery(self.drone)
        return True
