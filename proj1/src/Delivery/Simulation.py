from typing import List
from copy import deepcopy

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
    
    def greedySolve(self):
        while not self.all_orders_complete():
            attr_count = 0
            for drone in self.drones:
                attr_count += self.bestShipment(drone)
            if attr_count == 0:
                break
        
        print(self.evaluate())
        
    
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
                    if shipment.hasProducts():
                        shipments.append(shipment)
        if len(shipments) == 0:
            return 0
        shipments = sorted(shipments, key=lambda sh : -sh.score)
        shipments[0].execute()
        return 1

    def evaluate(self):
        commands = []
        for drone in self.drones:
            commands += [cmd.command_str for cmd in drone.commands]
        print(commands)
        return evaluate(len(self.drones), self.max_turns, self.drones[0].max_capacity, self.i_warehouses, self.i_orders, self.products, commands)
