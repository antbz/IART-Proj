from Delivery.Drone import Drone
from Delivery.Shipment import Shipment


def swap_drones(sh1: Shipment, sh2: Shipment, condition: bool):
    max_turns = sh1.drone.max_turns
    d1_turns = sh1.drone.turn - sh1.turns + sh2.turns
    d2_turns = sh2.drone.turn - sh2.turns + sh1.turns
    if not condition or (d1_turns <= max_turns and d2_turns <= max_turns):
        sh1_drone = sh1.drone
        sh1_drone.turn = d1_turns
        sh2_drone = sh2.drone
        sh2_drone.turn = d2_turns

        sh1.drone = sh2_drone
        sh2.drone = sh1_drone
        return True
    return False


def change_sh_drone(sh: Shipment, d: Drone, condition: bool):
    d_turns = d.turn + sh.turns
    if not condition or (d_turns <= d.max_turns):
        sh.drone.turn -= sh.turns
        d.turn = d_turns
        sh.drone = d
        return True
    return False
