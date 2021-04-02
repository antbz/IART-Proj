from time import time
from typing import List

from delivery.chromosome import Chromosome
from delivery.command import Command
from delivery.drone import Drone
from delivery.order import Order
from delivery.shipment import Shipment
from delivery.warehouse import Warehouse
from evaluate import evaluate


class Simulation:
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        self.max_turns = max_turns
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_drones = len(drones)
        self.max_cargo = drones[0].max_capacity
        self.products = products
        self.chromosome: Chromosome = Chromosome(drones, orders, warehouses)
        self.i_drones: List[Drone] = drones
        self.i_orders: List[Order] = orders
        self.i_warehouses: List[Warehouse] = warehouses

    def __repr__(self):
        return f"Simulation\n" \
               f"max turns: {self.max_turns}\n" \
               f"num rows: {self.num_rows}\n" \
               f"num cols: {self.num_cols}\n" \
               f"products: {self.products}\n" \
               f"drones: {self.i_drones}\n" \
               f"orders: {self.i_orders}\n" \
               f"warehouses: {self.i_warehouses}\n"

    def solve(self, out_file: str, num_itr: int = 1):
        start = time()

        for n in range(num_itr):
            self.algorithm()

        print(f"\nSolving took: {time() - start}")

        score, max_turn, average = self.evaluate()
        print(f"Total score: {score}")
        print(f"Number of turns: {max_turn}")
        print(f"Average order's score: {average}")

        self.chromosome.write_to_file(out_file)

    def evaluate(self):
        self.chromosome.getCommands()
        return evaluate(self, self.chromosome.commands)

    def evaluate_shipments(self, shipments):
        return evaluate(self, self.chromosome.getCommandsFromShipments(shipments))

    def execute_commands(self, commands: List[str]):
        current_sh = []
        for cmd in [c.split() for c in commands]:
            if cmd[1] == 'L' and len(current_sh) != 0 and current_sh[-1].type == 'D':
                shipment = Shipment.fromcommands(current_sh)
                shipment.execute()
                self.chromosome.shipments.append(shipment)
                current_sh.clear()
            if cmd[1] == 'L':
                current_sh.append(Command('L', self.chromosome.drones[int(cmd[0])], self.chromosome.warehouses[int(cmd[2])], self.products[int(cmd[3])], int(cmd[4])))
            elif cmd[1] == 'D':
                current_sh.append(Command('D', self.chromosome.drones[int(cmd[0])], self.chromosome.orders[int(cmd[2])], self.products[int(cmd[3])], int(cmd[4])))
        shipment = Shipment.fromcommands(current_sh)
        shipment.execute()
        self.chromosome.shipments.append(shipment)
