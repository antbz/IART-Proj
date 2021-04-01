from copy import deepcopy
from typing import List
from Delivery.Command import Command

from Delivery.Drone import Drone
from Delivery.Order import Order
from Delivery.Shipment import Shipment
from Delivery.Warehouse import Warehouse
from Evaluate import evaluate


class Chromossome:
    def __init__(self, drones, orders, warehouses):
        self.drones: List[Drone] = deepcopy(drones)
        self.orders: List[Order] = deepcopy(orders)
        self.warehouses: List[Warehouse] = deepcopy(warehouses)
        self.shipments: List[Shipment] = []
    
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

    