import sys
from pathlib import Path

from delivery.genetic import GeneticSimulation
from delivery.greedy import GreedySimulation
from delivery.hill_climbing import HillClimbing
from delivery.randoms import RandomSimulation
from delivery.sim_annealing import SASimulation
from evaluate import fileToCommands
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

    # Random
    if option == 1:
        simulation.__class__ = RandomSimulation
        simulation.solve("../output/" + out_file)

    # Greedy
    if option == 2:
        simulation.__class__ = GreedySimulation
        simulation.solve("../output/" + out_file)

    # HC, SA or RecursiveSA
    elif option in [3, 4, 5]:
        init_sol_file = init_sol_menu()
        if init_sol_file == "*":
            return False

        if option == 3:
            simulation.__class__ = HillClimbing
        else:
            simulation.__class__ = SASimulation

        n = 1
        if option == 5:
            n = number("Enter the number of iterations (0 to cancel): ")
            if n == 0:
                return False

        simulation.execute_commands(fileToCommands("../output/" + init_sol_file))
        simulation.solve("../output/" + out_file, n)

    # Genetic
    elif option == 6:
        simulation.__class__ = GeneticSimulation
        simulation.solve("../output/" + out_file)

    press()
    return True


def run_eval():
    print("\n===Evaluate===")
    input_file = in_menu()
    if input_file == "*":
        return

    out_file = out_menu()
    if out_file == "*":
        return

    simulation = parseInput("../input/" + input_file)
    score, max_turn, average = evaluate(simulation, fileToCommands("../output/" + out_file))

    print(f"\nTotal score: {score}")
    print(f"Number of turns: {max_turn}")
    print(f"Average orders' score: {average}")

    press()
    return


def alg_menu():
    while True:
        print("\nChoose the algorithm:")
        print("[1] Random")
        print("[2] Greedy")
        print("[3] Hill Climbing (random)")
        print("[4] Simulated Annealing")
        print("[5] Recursive Simulated Annealing")
        print("[6] Genetic")
        print("[0] Back")
        while True:
            option_alg = input("\nEnter your option: ")
            if option_alg == "0":
                return
            elif option_alg == "1":
                print("\n===Random===")
            elif option_alg == "2":
                print("\n===Greedy===")
            elif option_alg == "3":
                print("\n===Hill Climbing===")
            elif option_alg == "4":
                print("\n===Simulated Annealing===")
            elif option_alg == "5":
                print("\n===Recursive Simulated Annealing===")
            elif option_alg == "6":
                print("\n===Genetic===")
            else:
                print("Invalid option. Try again!")
                continue

            if run_solve(int(option_alg)):
                return
            else:
                break


def main_menu():
    while True:
        print("\nWelcome to the delivery problem!")
        print("Choose the mode:")
        print("[1] Solve")
        print("[2] Evaluate")
        print("[0] Exit the program")
        while True:
            option_main = input("\nEnter your option: ")
            if option_main == "1":
                alg_menu()
                break
            elif option_main == "2":
                run_eval()
                break
            elif option_main == "0":
                leave()
            else:
                print("Invalid option. Try again!")


if __name__ == "__main__":
    main_menu()
