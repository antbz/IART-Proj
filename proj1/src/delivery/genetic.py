import concurrent.futures as cf
from copy import deepcopy
from math import ceil
from random import choice, randrange, sample, random
from typing import List

import numpy.random as npr

from delivery.chromosome import Chromosome
from delivery.drone import Drone
from delivery.mutations import swap_drones, change_sh_drone
from delivery.shipment import Shipment
from delivery.simulation import Simulation

POPULATION_SIZE = 50
MAX_ITER = 30


class GeneticSimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def generate_population(self):
        print("\nGenerating initial population...")
        with cf.ThreadPoolExecutor() as executor:
            future_list = [executor.submit(self.generate_chromosome) for i in range(POPULATION_SIZE)]
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
        print(f"Initial population's average score {sum([c.score for c in self.population]) / POPULATION_SIZE}")
        print(f"Best chromosome's score: {self.best_chromosome().score}")

        for i in range(MAX_ITER):
            print(f"\nIteration number {i + 1}")
            children = self.generate_offspring()
            new_population = self.population + children
            self.mutate_population(new_population)
            self.population = list(
                npr.choice(new_population, size=POPULATION_SIZE, p=self.roullete_weights(new_population),
                           replace=False))

            print(f"Current population's average score {sum([c.score for c in self.population]) / POPULATION_SIZE}")
            print(f"Best chromosome's score: {self.best_chromosome().score}")

        self.chromosome = self.best_chromosome()
        self.chromosome.prune()

    def randomShipment(self, chromosome: Chromosome, drone: Drone):
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
            couples = [npr.choice(self.population, size=2, p=roullete, replace=False) for c in
                       range(int(len(self.population) / 20))]
            copulators = executor.map(self.crossover, couples)
            for c in copulators:
                children.extend(c)
        return children

    def mutate_population(self, population: List[Chromosome]):
        with cf.ThreadPoolExecutor() as executor:
            mutated = npr.choice(self.population, size=ceil(len(population) / 5), replace=False)
            for m in executor.map(self.mutate, mutated):
                population.append(m)

    def roullete_weights(self, population: List[Chromosome]):
        weights = [p.score for p in population]
        t_weight = sum(weights)
        return [w / t_weight for w in weights]

    def crossover(self, couple):
        # Copy parent chromosomes
        c1: Chromosome = deepcopy(couple[0])
        c2: Chromosome = deepcopy(couple[1])

        c1_sh_num = len(c1.shipments)
        c2_sh_num = len(c2.shipments)

        # Two point crossover
        # Select segment size
        seg_size = min(randrange(ceil(min([c1_sh_num, c2_sh_num]) / 5)) + 1, 10)

        # Select start and end points for crossover
        c1_start = randrange(c1_sh_num - seg_size + 1)
        c1_end = c1_start + seg_size
        c2_start = randrange(c2_sh_num - seg_size + 1)
        c2_end = c2_start + seg_size

        # Extract slice from parents
        seg_1 = c1.shipments[c1_start:c1_end]
        seg_2 = c2.shipments[c2_start:c2_end]

        # Recombination - insert other parent's slice into
        # child. Also makes sure objects are consistent
        self.recombine(c1, seg_2, c1_start, c1_end)
        self.recombine(c2, seg_1, c2_start, c2_end)

        # Calculate score for each child and mark
        # constraint violations as inactive
        c1.score = self.evaluate_child(c1)
        c2.score = self.evaluate_child(c2)
        return c1, c2

    def recombine(self, chromosome: Chromosome, slice: List[Shipment], start: int, end: int):
        for sh in slice:
            sh.drone = chromosome.drones[sh.drone.id]
            sh.order = chromosome.orders[sh.order.id]
            sh.warehouse = chromosome.warehouses[sh.warehouse.id]

        chromosome.shipments[start:end] = slice

    def mutate(self, chromosome: Chromosome):
        mutated = deepcopy(chromosome)
        for i in range(10):
            if random() >= 0.5 and len(mutated.shipments) > 1:
                sh1, sh2 = sample(mutated.shipments, k=2)
                if swap_drones(sh1, sh2, True):
                    break
            else:
                sh = choice(mutated.shipments)
                d = choice(mutated.drones)
                if change_sh_drone(sh, d, True):
                    break

        mutated.score = self.evaluate_child(mutated)
        return mutated

    def evaluate_child(self, child: Chromosome):
        for ord in child.orders:
            ord.remove_all_products()
            ord.add_products(self.i_orders[ord.id].products)
            ord.clear_deliveries()
        for wh in child.warehouses:
            wh.remove_all_products()
            wh.add_products(self.i_warehouses[wh.id].products)
        for d in child.drones:
            d.turn = 0
            d.set_position(child.warehouses[0].position)

        score = 0
        for sh in child.shipments:
            before = sh.order.is_complete()
            sh.calculate_turns()
            sh.is_active = sh.execute()
            if not sh.is_active:
                score -= 0
            if not before and sh.is_active and sh.order.is_complete():
                o_score = ceil(100 * (self.max_turns - max(sh.order.deliveries) + 1) / self.max_turns)
                score += o_score
        return score

    def best_chromosome(self):
        return max(self.population, key=lambda c: c.score)
