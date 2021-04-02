from copy import deepcopy
from random import choice, random, sample

from Delivery.Mutations import swap_drones, change_sh_drone
from Delivery.Simulation import Simulation

MAX_ITER = 300


class HillClimbing(Simulation):
    def __init__(self, max_turns, num_rows, num_cols, products, drones, orders, warehouses):
        super().__init__(max_turns, num_rows, num_cols, products, drones, orders, warehouses)

    def algorithm(self):
        self.current = self.evaluate()[0]
        self.current_shipments = deepcopy(self.chromosome.shipments)
        best = self.current
        print(f"\nInitial score: {best}")

        for t in range(MAX_ITER):
            new_score, new_shipments = self.random_neighbor()

            if new_score > self.current:
                print(f"New score: {new_score}")
                self.current_shipments = new_shipments
                self.current = new_score
            if new_score > best:
                best = new_score
                self.chromosome.shipments = new_shipments

    def random_neighbor(self):
        if len(self.current_shipments) == 1:
            raise ValueError("Cannot use permutation on single shipments")

        mutated_sh = deepcopy(self.current_shipments)
        mutated = False
        for i in range(10):
            if random() >= 0.5:
                sh1, sh2 = sample(mutated_sh, k=2)
                if swap_drones(sh1, sh2, True):
                    mutated = True
                    break
            else:
                sh = choice(mutated_sh)
                d = choice(self.chromosome.drones)
                if change_sh_drone(sh, d, True):
                    mutated = True
                    break

        if mutated:
            return self.evaluate_shipments(mutated_sh)[0], mutated_sh

        return self.current, mutated_sh
