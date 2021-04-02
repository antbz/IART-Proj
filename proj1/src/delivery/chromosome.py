from copy import deepcopy
from typing import List

from delivery.drone import Drone
from delivery.order import Order
from delivery.shipment import Shipment
from delivery.warehouse import Warehouse


class Chromosome:
    def __init__(self, drones, orders, warehouses):
        self.drones: List[Drone] = deepcopy(drones)
        self.orders: List[Order] = deepcopy(orders)
        self.warehouses: List[Warehouse] = deepcopy(warehouses)
        self.shipments: List[Shipment] = []
        self.score = 0

    def all_orders_complete(self):
        self.incomplete_orders = [o for o in self.orders if not o.is_complete()]
        return len(self.incomplete_orders) == 0

    def write_to_file(self, out_file):
        with open(out_file, mode='wt') as out:
            out.write(str(len(self.commands)))
            out.writelines(self.commands)

    def getCommands(self):
        self.commands = self.getCommandsFromShipments(self.shipments)
        return self.commands

    def getCommandsFromShipments(self, shipments: List[Shipment]):
        commands = []
        for shipment in shipments:
            commands += [cmd.command_str for cmd in shipment.commands]
        return commands

    def prune(self):
        self.shipments = [sh for sh in self.shipments if sh.is_active]
