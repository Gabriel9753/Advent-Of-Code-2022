import sys
from time import time
from loguru import logger
from aocd import get_data
import sympy
from time import time
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

monkeys = {}

def calc_for_monkey(monkey):
    job = monkeys[monkey]
    if isinstance(job, int):
        return job
    elif monkey == "root":
        splitted_job = job.split(" ")
        monkey_1 = splitted_job[0]
        monkey_2 = splitted_job[-1]
        _operator = splitted_job[1]
        return eval(f"{calc_for_monkey(monkey_1)} {_operator} {calc_for_monkey(monkey_2)}")
    else:
        splitted_job = job.split(" ")
        monkey_1 = splitted_job[0]
        monkey_2 = splitted_job[-1]
        _operator = splitted_job[1]
        return f"({calc_for_monkey(monkey_1)} {_operator} {calc_for_monkey(monkey_2)})"

def part_2(monkey):
    job = monkeys[monkey]
    if monkey == "humn":
        return "X"
    elif isinstance(job, int):
        return f"{job}"
    else:
        splitted_job = job.split(" ")
        monkey_1 = splitted_job[0]
        monkey_2 = splitted_job[-1]
        _operator = splitted_job[1]
        if monkey == "root":
            return f"{part_2(monkey_1)} = {part_2(monkey_2)}"
        else:
            return f"({part_2(monkey_1)} {_operator} {part_2(monkey_2)})"

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    for line in puzzle_input.splitlines():
        monkey = line.split(":")[0]
        _value = line.split(":")[1].strip()
        try:
            _value = int(_value)
        except ValueError:
            pass
        monkeys[monkey] = _value
    
    start = time()
    print(f"Part 1: {int(calc_for_monkey('root'))}")
    print(f"Time: {time() - start}")
    start = time()
    X = sympy.symbols('X')
    eq_string = part_2("root")
    equations = eq_string.split("=")
    eq_1, eq_2 = equations[0].strip(), equations[1].strip()
    equation = sympy.Eq(sympy.sympify(eq_1), sympy.sympify(eq_2))
    # Löse die Gleichung nach X
    solution = sympy.solve(equation, X)
    print(f"Part 2: {solution[0]}")
    print(f"Time: {time() - start}")

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
