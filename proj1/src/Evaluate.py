from typing import DefaultDict, Dict
from math import ceil

from Delivery.Product import *
from Delivery.Warehouse import *
from Delivery.Drone import *
from Delivery.Order import *


def evaluate(num_drones, max_time, max_cargo, wh_list, order_list, product_list, commands):
    warehouses: Dict[int, Warehouse] = {w.id: w for w in wh_list}
    orders: Dict[int, Order] = {o.id: o for o in order_list}
    products: Dict[int, Product] = {p.id: p for p in product_list}
    drones: Dict[int, Drone] = {
        i: Drone(id=i, position=warehouses[0].position, max_capacity=max_cargo, max_turns=max_time)
        for i in range(num_drones)
    }

    drone_to_delivery_time: Dict[Drone, int] = DefaultDict(int)
    order_to_delivery_time: Dict[Order, list] = DefaultDict(list)
    score = 0
    deliv_max = 0

    for i, command in enumerate(commands):
        drone_id, str_command, destination_id, product_id, quantity = command.split(" ")

        drone_id = int(drone_id)
        destination_id = int(destination_id)
        product_id = int(product_id)
        quantity = int(quantity)

        drone = drones[drone_id]
        product = products[product_id]
        basket = {product: quantity}

        if str_command == "L":
            warehouse = warehouses[destination_id]

            if warehouse.products.get(product, 0) < quantity:
                raise ValueError(f"Command {i}: {warehouse} have not enough {product}.")
            warehouse.remove_products(basket)

            drone.add_products(basket)
            if drone.product_weight > max_cargo:
                raise ValueError(f"Command {i}: {drone} overloaded.")

            drone_to_delivery_time[drone] += drone.distanceTo(warehouse) + 1
            drone.set_position(warehouse.position)

        elif str_command == "D":
            order = orders[destination_id]
            if order.is_complete():
                raise ValueError(
                    f"Command {i}: the {order} is closed, nothing can be delivered there."
                )

            if drone.products.get(product, 0) < quantity:
                raise ValueError(f"Command {i}: {drone} have not enough {product}.")
            drone.remove_products(basket)

            if order.products.get(product, 0) < quantity:
                raise ValueError(f"Command {i}: Too many {product} for {order}.")
            order.remove_products(basket)

            drone_to_delivery_time[drone] += drone.distanceTo(order) + 1
            drone.set_position(order.position)
            order_to_delivery_time[order].append(drone_to_delivery_time[drone]-1)

            if order.is_complete():
                delivery_time = max(order_to_delivery_time[order])
                if delivery_time > deliv_max:
                    deliv_max = delivery_time
                if delivery_time < max_time:
                    sc = ceil(100 * (max_time - delivery_time) / max_time)
                    score += sc
                    # print(str(order.id) + " scored: " + str(sc))
                else:
                    raise ValueError(f"Command {i}: Run out of time.")
        else:
            raise ValueError(f"Command {i}: Unknown command {str_command}.")
    print(f"Max turn: {deliv_max}")
    print(f"Total score: {score}")
    return score


def fileToCommands(path):
    with open(path) as f:
        commands = []
        lines = f.readlines()
        num_lines = int(lines[0])
        for i in range(1, num_lines + 1):
            commands.append(lines[i].strip())
    return commands
