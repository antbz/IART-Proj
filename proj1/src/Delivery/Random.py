from typing import List
from random import choice
from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation

class RandomSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)
    
    def algorithm(self):
        while not self.all_orders_complete():
            attr_count = 0
            for drone in self.drones:
                attr_count += self.randomShipment(drone)
                if self.all_orders_complete():
                    return
            if attr_count == 0:
                break

    def randomShipment(self, drone: Drone):
        order = choice(self.incomplete_orders)
        possible_sh = [sh for wh in self.warehouses if (sh := Shipment.fromdow(drone, order, wh)).hasProducts()]
        if len(possible_sh) == 0:
            return 0
        shipment = choice(possible_sh)
        shipment.execute()
        self.shipments.append(shipment)
        return 1
