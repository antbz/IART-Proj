from copy import deepcopy
from typing import List
from random import choice
from Delivery.Chromossome import Chromossome
from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation
import concurrent.futures

class GeneticSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def generate_population(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_list = [executor.submit(self.generate_chromossome) for i in range(10)]
            self.population = [f.result() for f in concurrent.futures.as_completed(future_list)]
            print(len(self.population))
            self.chromossome = self.population[0]

    def generate_chromossome(self):
        chromossome = deepcopy(self.chromossome)
        while not chromossome.all_orders_complete():
            attr_count = 0
            for drone in chromossome.drones:
                attr_count += self.randomShipment(chromossome, drone)
                if chromossome.all_orders_complete():
                    return chromossome
            if attr_count == 0:
                break
        return chromossome
    
    def algorithm(self):
        self.generate_population()

    def randomShipment(self, chromossome : Chromossome, drone: Drone):
        order = choice(chromossome.incomplete_orders)
        possible_sh = [sh for wh in chromossome.warehouses if (sh := Shipment.fromdow(drone, order, wh)).hasProducts()]
        if len(possible_sh) == 0:
            return 0
        shipment = choice(possible_sh)
        shipment.execute()
        chromossome.shipments.append(shipment)
        return 1
