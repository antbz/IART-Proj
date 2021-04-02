from random import choice, sample

from delivery.drone import Drone
from delivery.shipment import Shipment
from delivery.simulation import Simulation


class RandomSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        print("\nGenerating solution...")
        while not self.chromosome.all_orders_complete():
            attr_count = 0
            for drone in self.chromosome.drones:
                attr_count += self.randomShipment(drone)
                if self.chromosome.all_orders_complete():
                    break
            if attr_count == 0:
                break

    def randomShipment(self, drone: Drone):
        order = choice(self.chromosome.incomplete_orders)
        wh_sample = sample(self.chromosome.warehouses, k=len(self.chromosome.warehouses))
        for wh in wh_sample:
            sh = Shipment.fromdow(drone, order, wh)
            if sh.hasProducts():
                sh.execute()
                self.chromosome.shipments.append(sh)
                return 1
        return 0
