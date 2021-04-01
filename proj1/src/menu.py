import sys

from Delivery.Genetic import GeneticSimulation
from Delivery.Greedy import GreedySimulation
from Delivery.SimAnnealing import SASimulation
from Evaluate import fileToCommands
from file import *


def leave():
    print("Quitting the program. Goodbye!")
    sys.exit()


def in_menu():
    while True:
        input_file = str(input("Input file name (* to cancel): "))
        if input_file == "*":
            print("Cancelled. Going back!")
            break
        else:
            my_file = Path("../input/" + input_file)
            if my_file.is_file():
                break
            else:
                print("File does not exist, try again")
                continue
    return input_file


def out_menu():
    while True:
        out_file = str(input("Output file name (* to cancel): "))
        if out_file == "*":
            print("Cancelled. Going back!")
            break
        else:
            my_file = Path("../output/" + out_file)
            if my_file.is_file():
                break
            else:
                print("File does not exist, try again")
                continue
    return out_file


def init_sol_menu():
    while True:
        init_sol_file = str(input("Initial solution file (* to cancel): "))
        if init_sol_file == "*":
            print("Cancelled. Going back!")
            break
        else:
            my_file = Path("../output/" + init_sol_file)
            if my_file.is_file():
                break
            else:
                print("File does not exist, try again")
                continue
    return init_sol_file


def run_solve(option):
    if option == 3:
        print("Work in progress")
        sys.exit()
    else:
        input_file = in_menu()
        if input_file == "*":
            return False
        out_file = out_menu()
        if out_file == "*":
            return False
        simulation = parseInput("../input/" + input_file)
        if option == 1:
            simulation.__class__ = GreedySimulation
        elif option == 2:
            init_sol_file = init_sol_menu()
            if init_sol_file == "*":
                return False
            simulation.__class__ = SASimulation
            simulation.execute_commands(fileToCommands("../output/" + init_sol_file))
        simulation.solve("../output/" + out_file)
    return True


def run_eval():
    input_file = in_menu()
    if input_file == "*":
        return False
    out_file = out_menu()
    if out_file == "*":
        return False
    simulation = parseInput("../input/" + input_file)
    score, max_turn, average = evaluate(simulation, fileToCommands("../output/" + out_file))
    print(f"Total score: {score}")
    print(f"Number of turns: {max_turn}")
    print(f"Average score: {average}")
    return True


def alg_menu():
    ans = False
    print("\nChoose the algorithm:")
    print("[1] Greedy")
    print("[2] Simulated Annealing")
    print("[3] Genetic")
    print("[0] Back")
    while not ans:
        option_alg = int(input("\nEnter your option : "))
        if option_alg == 1:
            ans = True
            if not run_solve(1):
                alg_menu()
        elif option_alg == 2:
            ans = True
            if not run_solve(2):
                alg_menu()
        elif option_alg == 3:
            ans = True
            if not run_solve(3):
                alg_menu()
        elif option_alg == 0:
            ans = True
            main_menu()
        else:
            print("Invalid option. Try again!")


def main_menu():
    ans = False
    print("\nWelcome to the delivery problem!")
    print("Choose the mode:")
    print("[1] Solve")
    print("[2] Evaluate")
    print("[0] Exit the program")
    while not ans:
        option_main = int(input("\nEnter your option: "))
        if option_main == 1:
            ans = True
            alg_menu()
        elif option_main == 2:
            ans = True
            if not run_eval():
                main_menu()
        elif option_main == 0:
            ans = True
            leave()
        else:
            print("Invalid option. Try again!")
