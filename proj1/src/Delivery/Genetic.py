from copy import deepcopy
from typing import List
from random import choice
from Delivery.Chromosome import Chromosome
from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation
import concurrent.futures

class GeneticSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def generate_population(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_list = [executor.submit(self.generate_chromosome) for i in range(10)]
            self.population = [f.result() for f in concurrent.futures.as_completed(future_list)]
            print(len(self.population))
            self.chromosome = self.population[0]

    def generate_chromosome(self):
        chromosome = deepcopy(self.chromosome)
        while not chromosome.all_orders_complete():
            attr_count = 0
            for drone in chromosome.drones:
                attr_count += self.randomShipment(chromosome, drone)
                if chromosome.all_orders_complete():
                    return chromosome
            if attr_count == 0:
                break
        return chromosome
    
    def algorithm(self):
        self.generate_population()

    def randomShipment(self, chromosome : Chromosome, drone: Drone):
        order = choice(chromosome.incomplete_orders)
        possible_sh = [sh for wh in chromosome.warehouses if (sh := Shipment.fromdow(drone, order, wh)).hasProducts()]
        if len(possible_sh) == 0:
            return 0
        shipment = choice(possible_sh)
        shipment.execute()
        chromosome.shipments.append(shipment)
        return 1
