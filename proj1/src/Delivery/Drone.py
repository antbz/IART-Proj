from typing import List, Tuple
from random import randrange

from Delivery.ProductContainer import ProductContainer


class Drone(ProductContainer):
    def __init__(self, id, max_capacity, max_turns, position):
        super().__init__(id, position)
        self.max_capacity = max_capacity
        self.max_turns = max_turns
        self.used_capacity = 0
        self.shipments = []
        self.turn = 0

    def __repr__(self):
        return f"Drone(id: {self.id}; position: {self.position}; max_capacity: {self.max_capacity}; products: {self.products} shipments: {self.shipments}); "

    def set_position(self, position: Tuple):
        self.position = position

    def add_shipment(self, shipment):
        self.shipments.append(shipment)

    @property
    def commands(self):
        commands = []
        for shipment in self.shipments:
            commands += shipment.commands
        return commands

    def add_turns(self, turns):
        self.turn += turns
    
    def swap_with(self, drone : "Drone"):
        for i in range(len(self.shipments) * len(drone.shipments)):
            s1_idx = randrange(len(self.shipments))
            s1 = self.shipments[s1_idx]
            s2_idx = randrange(len(drone.shipments))
            s2 = drone.shipments[s2_idx]
            d1_turns = self.turn - s1.turns + s2.turns
            d2_turns = drone.turn - s2.turns + s1.turns
            if (d1_turns <= self.max_turns and d2_turns <= self.max_turns):
                s2.drone = self
                self.shipments[s1_idx] = s2
                self.turn = d1_turns
                s1.drone = drone
                drone.shipments[s2_idx] = s1
                drone.turn = d2_turns
                return True
        return False



        
