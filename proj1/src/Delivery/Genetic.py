from copy import deepcopy
from typing import List
from random import choice, sample
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
            future_list = [executor.submit(self.generate_chromosome) for i in range(100)]
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
        wh_sample = sample(chromosome.warehouses, k=len(chromosome.warehouses))
        for wh in wh_sample:
            sh = Shipment.fromdow(drone, order, wh)
            if sh.hasProducts():
                sh.execute()
                chromosome.shipments.append(sh)
                return 1
        return 0
