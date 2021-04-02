from copy import deepcopy
from math import ceil
from os import replace
from typing import List
from random import choice, randrange, sample
from Delivery.Chromosome import Chromosome
from Delivery.Drone import Drone
from Delivery.Shipment import Shipment
from Delivery.Simulation import Simulation
import numpy.random as npr
import concurrent.futures as cf

class GeneticSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def generate_population(self):
        with cf.ThreadPoolExecutor() as executor:
            future_list = [executor.submit(self.generate_chromosome) for i in range(20)]
            self.population = [f.result() for f in cf.as_completed(future_list)]

    def generate_chromosome(self):
        chromosome = deepcopy(self.chromosome)
        while not chromosome.all_orders_complete():
            attr_count = 0
            for drone in chromosome.drones:
                attr_count += self.randomShipment(chromosome, drone)
                if chromosome.all_orders_complete():
                    chromosome.score = self.evaluate_shipments(chromosome.shipments)[0]
                    return chromosome
            if attr_count == 0:
                break
        chromosome.score = self.evaluate_shipments(chromosome.shipments)[0]
        return chromosome
    
    def algorithm(self):
        self.generate_population()

        for i in range(10):
            print(i)
            children = self.generate_offspring()
            new_population = self.population + children
            self.population = list(npr.choice(new_population, size=len(self.population), p=self.roullete_weights(new_population), replace=False))
            
        self.chromosome = self.best_chromossome()

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

    def generate_offspring(self):
        roullete = self.roullete_weights(self.population)
        children = []
        with cf.ThreadPoolExecutor() as executor:
            couples = [npr.choice(self.population, size=2, p=roullete, replace=False) for c in range(int(len(self.population) / 3))]
            copulators = executor.map(self.crossover, couples)
            # copulators = [executor.submit(self.crossover(c)) for c in couples]
            for c in copulators:
                children.extend(c)
        return children
    
    def roullete_weights(self, population: List[Chromosome]):
        weights = [p.score for p in population]
        t_weight = sum(weights)
        return [w / t_weight for w in weights]

    def crossover(self, couple):
        # Copy parent chromossomes
        c1 : Chromosome = deepcopy(couple[0])
        c2 : Chromosome = deepcopy(couple[1])
        
        # Two point crossover
        # Select start and end points from chromossome
        start = randrange(len(c1.shipments))
        end = randrange(start, len(c1.shipments))
        # Extract slice from parents
        seq_1 = c1.shipments[start:end + 1]
        seq_2 = c2.shipments[start:end + 1]
        # Recombination - insert other parent's slice into
        # child. Also makes sure objects are consistent
        self.recombine(c1, seq_2, start, end)
        self.recombine(c2, seq_1, start, end)
        
        # Calculate score for each child and mark
        # constraint violations as inactive
        c1.score = self.evaluate_child(c1)
        c2.score = self.evaluate_child(c2)
        return c1, c2

    def recombine(self, chromossome: Chromosome, slice: List[Shipment], start: int, end: int):
        for sh in slice:
            sh.drone = chromossome.drones[sh.drone.id]
            sh.order = chromossome.orders[sh.order.id]
            sh.warehouse = chromossome.warehouses[sh.warehouse.id]
        chromossome.shipments[start:end+1] = slice
    
    def evaluate_child(self, child: Chromosome):
        score = 0
        for sh in child.shipments:
            sh.calculate_turns()
            sh.is_active = sh.execute()
            if sh.order.is_complete():
                score += ceil((self.max_turns - sh.drone.turn) / self.max_turns)
        return score

    def best_chromossome(self):
        best = max(self.population, key=lambda p: p.score)
        best.prune()
        return best
