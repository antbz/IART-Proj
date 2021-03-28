from math import exp
from typing import List
from copy import deepcopy
from time import time
from random import random, randrange

from Delivery.Drone import Drone
from Delivery.Order import Order
from Delivery.Shipment import Shipment
from Delivery.Warehouse import Warehouse
from Evaluate import evaluate


class Simulation:
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        self.max_turns = max_turns
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.products = products
        self.drones : List[Drone] = drones
        self.orders : List[Order] = orders
        self.i_orders : List[Order] = deepcopy(orders)
        self.warehouses : List[Warehouse] = warehouses
        self.i_warehouses : List[Warehouse] = deepcopy(warehouses)

    def __str__(self):
        return f"Simulation\n" \
               f"max turns: {self.max_turns}\n" \
               f"num rows: {self.num_rows}\n" \
               f"num cols: {self.num_cols}\n" \
               f"products: {self.products}\n" \
               f"drones: {self.drones}\n" \
               f"orders: {self.orders}\n" \
               f"warehouses: {self.warehouses}\n"

    def solve(self, out_file : str, algorithm):
        start = time()
        algorithm()
        print(f"Solving took: {time() - start}")

        commands = self.getCommands()
        self.evaluate(commands)
        with open(out_file, mode='wt') as out:
            out.write(str(len(commands)))
            out.writelines(commands)
    
    def solveGreedy(self):
        while not self.all_orders_complete():
            attr_count = 0
            for drone in self.drones:
                attr_count += self.bestShipment(drone)
            if attr_count == 0:
                break
        
    def solveSA(self):
        self.solveGreedy()
        T0 = 100

        self.best = self.evaluate(self.getCommands())

        for t in range(100):
            T = self.cooldown(T0, t)
            new_score, new_drones = self.random_neighbor()
            if (new_score > self.best or exp((new_score - self.best) / T) >= random()):
                self.drones = new_drones
                self.best = new_score

    def cooldown(self, T0, t):
        return T0 / (1 + 0.05 * t ** 2)

    def random_neighbor(self):
        if len(self.drones) == 1:
            raise ValueError("Cannot use permutation on single drone solutions")
        
        drones = deepcopy(self.drones)
        
        for i in range(len(drones)):
            d1_idx = randrange(len(drones))
            d1 = drones[d1_idx]
            for j in range(len(drones)):
                d2_idx = randrange(len(drones))
                if (d1_idx == d2_idx):
                    continue
                d2 = drones[d2_idx]
                if (d1.swap_with(d2)):
                    score = self.evaluate(self.getCommandsFromDrones(drones))
                    return score, drones

        return self.best, drones

    
    def all_orders_complete(self):
        for order in self.orders:
            if not order.is_complete():
                return False
        return True

    def bestShipment(self, drone : Drone):
        shipments : List[Shipment] = []
        for order in self.orders:
            if not order.is_complete():
                for wh in self.warehouses:
                    shipment = Shipment(drone, order, wh)
                    if shipment.hasProducts() and drone.turn + shipment.turns <= self.max_turns:
                        shipments.append(shipment)
        if len(shipments) == 0:
            return 0
        shipments = sorted(shipments, key=lambda sh : -sh.score)
        shipments[0].execute()
        return 1

    def getCommands(self):
        commands = []
        for drone in self.drones:
            commands += [cmd.command_str for cmd in drone.commands]
        return commands
    
    def getCommandsFromDrones(self, drones):
        commands = []
        for drone in drones:
            commands += [cmd.command_str for cmd in drone.commands]
        return commands

    def evaluate(self, commands):
        return evaluate(len(self.drones), self.max_turns, self.drones[0].max_capacity, deepcopy(self.i_warehouses), deepcopy(self.i_orders), self.products, commands)
