import sys
from pathlib import Path

from Delivery.Genetic import GeneticSimulation
from Delivery.Greedy import GreedySimulation
from Delivery.SimAnnealing import SASimulation
from Evaluate import fileToCommands
from file import *


def leave():
    print("Quitting the program. Goodbye!")
    sys.exit()


def press():
    input("\nPress Enter to continue...")


def number(text: str):
    n = input(text)
    while not n.isdigit():
        n = input("Not a number, try again: ")
    return int(n)


def in_menu():
    while True:
        input_file = input("Input file name (* to cancel): ")
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
    out_file = input("Output file name (* to cancel): ")
    if out_file == "*":
        print("Cancelled. Going back!")
    return out_file


def init_sol_menu():
    while True:
        init_sol_file = input("Initial solution file (* to cancel): ")
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
    input_file = in_menu()
    if input_file == "*":
        return False

    out_file = out_menu()
    if out_file == "*":
        return False

    simulation = parseInput("../input/" + input_file)

    # Greedy
    if option == 1:
        simulation.__class__ = GreedySimulation
        simulation.solve("../output/" + out_file)

    # SA or RecursiveSA
    elif option == 2 or option == 3:
        init_sol_file = init_sol_menu()
        if init_sol_file == "*":
            return False

        simulation.__class__ = SASimulation

        n = 1
        if option == 3:
            n = number("Enter the number of iterations (0 to cancel): ")
            if n == 0:
                return False

        simulation.execute_commands(fileToCommands("../output/" + init_sol_file))
        simulation.solve("../output/" + out_file, n)

    # Genetic
    elif option == 4:
        simulation.__class__ = GeneticSimulation
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

    print(f"\nTotal score: {score}")
    print(f"Number of turns: {max_turn}")
    print(f"Average score: {average}")
    return True


def alg_menu():
    while True:
        print("\nChoose the algorithm:")
        print("[1] Greedy")
        print("[2] Simulated Annealing")
        print("[3] Recursive Simulated Annealing")
        print("[4] Genetic")
        print("[0] Back")
        while True:
            option_alg = input("\nEnter your option: ")
            if option_alg == "0":
                return False
            elif option_alg == "1":
                print("\n===Greedy===")
            elif option_alg == "2":
                print("\n===Simulated Annealing===")
            elif option_alg == "3":
                print("\n===Recursive Simulated Annealing===")
            elif option_alg == "4":
                print("\n===Recursive Simulated Annealing===")
            else:
                print("Invalid option. Try again!")
                continue

            if run_solve(int(option_alg)):
                return True
            else:
                break


if __name__ == "__main__":
    while True:
        print("\nWelcome to the delivery problem!")
        print("Choose the mode:")
        print("[1] Solve")
        print("[2] Evaluate")
        print("[0] Exit the program")
        while True:
            option_main = input("\nEnter your option: ")
            if option_main == "1":
                if alg_menu():
                    press()
                break
            elif option_main == "2":
                if run_eval():
                    press()
                break
            elif option_main == "0":
                leave()
            else:
                print("Invalid option. Try again!")
