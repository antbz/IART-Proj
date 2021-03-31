from math import exp, log
from copy import deepcopy
from random import random, randrange

from Delivery.Simulation import Simulation

MAX_ITER = 10000

class SASimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        T0 = 100

        self.best = self.evaluate()[0]
        print(f"Initial: {self.best}")

        for t in range(MAX_ITER):
            T = self.cooldown(T0, t)
            if T < 1e-3:
                break
            new_score, new_drones = self.random_neighbor()
            if (new_score > self.best or exp((new_score - self.best) / T) >= random()):
                print(f"New score: {new_score}")
                self.drones = new_drones
                self.best = new_score

    def cooldown(self, T0, t):
        return self.quadratic_cooling(T0, t)

    def exponential_cooling(self, T0, t):
        return T0 * 0.8 ** t
    
    def log_cooling(self, T0, t):
        return T0 / (1 + log(1 + t))

    def linear_cooling(self, T0, t):
        return T0 / (1 + t)
    
    def quadratic_cooling(self, T0, t):
        return T0 / (1 + t ** 2)
    
    def random_neighbor(self):
        if len(self.drones) == 1:
            raise ValueError("Cannot use permutation on single drone solutions")
        
        drones = deepcopy(self.drones)
        
        for i in range(len(drones)):
            d1_idx = randrange(len(drones))
            d1 = drones[d1_idx]
            for j in range(len(drones)):
                d2_idx = randrange(len(drones))
                if (d1_idx == d2_idx):
                    continue
                d2 = drones[d2_idx]
                if (d1.swap_with(d2)):
                    score = self.evaluate_drones(drones)[0]
                    return score, drones

        return self.best, drones