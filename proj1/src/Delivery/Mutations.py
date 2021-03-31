from Delivery.Shipment import Shipment


def swap_drones(sh1 : Shipment, sh2 : Shipment):
    max_turns = sh1.drone.max_turns
    d1_turns = sh1.drone.turn - sh1.turns + sh2.turns
    d2_turns = sh2.drone.turn - sh2.turns + sh1.turns
    if (d1_turns <= max_turns and d2_turns <= max_turns):
        sh1_drone = sh1.drone
        sh1_drone.turn = d1_turns
        sh2_drone = sh2.drone
        sh2_drone.turn = d2_turns

        sh1.drone = sh2.drone
        sh2.drone = sh1_drone
        return True
    return False
