from collections import Counter

from delivery.product import *
from delivery.simulation import *
from delivery.warehouse import *


def parseInput(path):
    with open(path) as f:
        num_rows, num_cols, num_drones, max_turns, max_capacity = map(
            int, f.readline().split(" ")
        )

        # Read products
        num_products = int(f.readline())
        product_weights = list(map(int, f.readline().split(" ")))
        assert num_products == len(product_weights)
        products = [Product(i, w) for i, w in enumerate(product_weights)]

        # Read warehouses
        num_warehouses = int(f.readline())
        warehouses = []
        for i in range(num_warehouses):
            x, y = map(int, f.readline().split(" "))
            wh_stock = list(map(int, f.readline().split(" ")))
            assert num_products == len(wh_stock)
            wh_stock = {p: n for p, n in zip(products, wh_stock)}
            warehouses.append(Warehouse(id=i, position=(x, y), products=wh_stock))

        # Create drones
        drones = [Drone(id, max_capacity, max_turns, warehouses[0].position) for id in range(num_drones)]

        # order info
        orders = []
        num_orders = int(f.readline())
        for i in range(num_orders):
            x, y = map(int, f.readline().split(" "))
            num_products_in_order = int(f.readline())
            order_products = [products[x] for x in list(map(int, f.readline().split(" ")))]
            assert num_products_in_order == len(order_products)
            orders.append(Order(id=i, position=(x, y), products=dict(Counter(order_products))))

    return Simulation(max_turns, num_rows, num_cols, products, drones, orders, warehouses)
