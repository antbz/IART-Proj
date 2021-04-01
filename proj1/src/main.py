import sys
from collections import Counter

from Delivery.Drone import *
from Delivery.Greedy import GreedySimulation
from Delivery.Order import *
from Delivery.Product import *
from Delivery.Random import RandomSimulation
from Delivery.SimAnnealing import SASimulation
from Delivery.Simulation import *
from Delivery.Warehouse import *
from Evaluate import fileToCommands, evaluate


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



if (len(sys.argv) < 4):
    raise ValueError("Invalid arguments\nUsage: python main.py <mode> <input_file>.in <output_file>.out <initial_sol>.out")

simulation = parseInput(sys.argv[2])
simulation.__class__ = RandomSimulation

if sys.argv[1] == "solve":
    # simulation.execute_commands(fileToCommands(sys.argv[4]))
    simulation.solve(sys.argv[3])
elif sys.argv[1] == "eval":
    score, max_turn, average = evaluate(simulation, fileToCommands(sys.argv[3]))
    print(f"Total score: {score}")
    print(f"Number of turns: {max_turn}")
    print(f"Average score: {average}")
