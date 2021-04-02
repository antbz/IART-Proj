from typing import List

from delivery.drone import Drone
from delivery.shipment import Shipment
from delivery.simulation import Simulation


class GreedySimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        print("\nGenerating solution...")
        while not self.chromosome.all_orders_complete():
            attr_count = 0
            for drone in self.chromosome.drones:
                attr_count += self.bestShipment(drone)
            if attr_count == 0:
                break

    def bestShipment(self, drone: Drone):
        shipments: List[Shipment] = []
        for order in self.chromosome.orders:
            if not order.is_complete():
                for wh in self.chromosome.warehouses:
                    shipment = Shipment.fromdow(drone, order, wh)
                    if shipment.hasProducts() and drone.turn + shipment.turns <= self.max_turns:
                        shipments.append(shipment)
        if len(shipments) == 0:
            return 0
        shipments = sorted(shipments, key=lambda sh: -sh.score)
        shipments[0].execute()
        self.chromosome.shipments.append(shipments[0])
        return 1
