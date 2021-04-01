from copy import deepcopy
from typing import List
from random import choice
from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation
import concurrent.futures

class GeneticSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    # def solve(self, path):
    #     print("babab")

    def generate_population(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_list = [executor.submit(self.generate_chromossome) for i in range(100)]
            self.population = [f.result() for f in concurrent.futures.as_completed(future_list)]
            print(len(self.population))
            self.shipments = self.population[0]

    def generate_chromossome(self):
        sim = deepcopy(self)
        while not sim.all_orders_complete():
            attr_count = 0
            for drone in sim.drones:
                attr_count += sim.randomShipment(drone)
                if sim.all_orders_complete():
                    return sim.shipments
            if attr_count == 0:
                break
        return sim.shipments
    
    def algorithm(self):
        self.generate_population()

    def randomShipment(self, drone: Drone):
        order = choice(self.incomplete_orders)
        possible_sh = [sh for wh in self.warehouses if (sh := Shipment.fromdow(drone, order, wh)).hasProducts()]
        if len(possible_sh) == 0:
            return 0
        shipment = choice(possible_sh)
        shipment.execute()
        self.shipments.append(shipment)
        return 1
