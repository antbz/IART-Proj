from math import exp, log
from typing import List
from copy import deepcopy
from time import time
from random import random, randrange
from Delivery.Command import Command

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
        self.num_drones = len(drones)
        self.max_cargo = drones[0].max_capacity
        self.products = products
        self.drones : List[Drone] = drones
        self.i_drones : List[Drone] = deepcopy(drones)
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

    def solve(self, out_file : str):
        start = time()
        self.algorithm()
        print(f"Solving took: {time() - start}")

        score, max_turn, average = self.evaluate()
        print(f"Total score: {score}")
        print(f"Number of turns: {max_turn}")
        print(f"Average score: {average}")

        with open(out_file, mode='wt') as out:
            out.write(str(len(self.commands)))
            out.writelines(self.commands)

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

    def evaluate(self):
        self.commands = self.getCommands()
        return evaluate(self, self.commands)

    def evaluate_drones(self, drones):
        return evaluate(self, self.getCommandsFromDrones(drones))

    def execute_commands(self, commands : List[str]):
        current_sh = []
        for cmd in [c.split() for c in commands]:
            if cmd[1] == 'L' and len(current_sh) != 0 and current_sh[-1].type == 'D':
                shipment = Shipment.fromcommands(current_sh)
                shipment.execute()
                current_sh.clear()
            if cmd[1] == 'L':
                current_sh.append(Command('L', self.drones[int(cmd[0])], self.warehouses[int(cmd[2])], self.products[int(cmd[3])], int(cmd[4])))
            elif cmd[1] == 'D':
                current_sh.append(Command('D', self.drones[int(cmd[0])], self.orders[int(cmd[2])], self.products[int(cmd[3])], int(cmd[4])))
        shipment = Shipment.fromcommands(current_sh)
        shipment.execute()
