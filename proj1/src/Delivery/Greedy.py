from typing import List

from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation


class GreedySimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        while not self.chromossome.all_orders_complete():
            attr_count = 0
            for drone in self.chromossome.drones:
                attr_count += self.bestShipment(drone)
            if attr_count == 0:
                break

    def bestShipment(self, drone: Drone):
        shipments: List[Shipment] = []
        for order in self.chromossome.orders:
            if not order.is_complete():
                for wh in self.chromossome.warehouses:
                    shipment = Shipment.fromdow(drone, order, wh)
                    if shipment.hasProducts() and drone.turn + shipment.turns <= self.max_turns:
                        shipments.append(shipment)
        if len(shipments) == 0:
            return 0
        shipments = sorted(shipments, key=lambda sh: -sh.score)
        shipments[0].execute()
        self.chromossome.shipments.append(shipments[0])
        return 1
