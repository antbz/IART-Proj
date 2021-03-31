from copy import deepcopy
from math import exp, log
from random import random, choices

from Delivery.Mutations import swap_drones
from Delivery.Simulation import Simulation

MAX_ITER = 10000


class SASimulation(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        T0 = 100

        self.current = self.evaluate()[0]
        initial_sh = deepcopy(self.shipments)
        best = self.current
        print(f"Initial: {best}")

        for t in range(MAX_ITER):
            T = self.cooldown(T0, t)
            if T < 1e-3:
                break
            new_score, new_shipments = self.random_neighbor()
            if (new_score > self.current or exp((new_score - self.current) / T) >= random()):
                print(f"New score: {new_score}")
                self.shipments = new_shipments
                self.current = new_score

        if self.current < best:
            self.shipments = initial_sh


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

        mutated_sh = deepcopy(self.shipments)

        for i in range(10):
            sh1, sh2 = choices(mutated_sh, k=2)

            if (swap_drones(sh1, sh2)):
                score = self.evaluate_shipments(mutated_sh)[0]
                return score, mutated_sh

        return self.current, mutated_sh
