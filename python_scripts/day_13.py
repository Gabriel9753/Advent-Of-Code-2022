import sys
from time import time
from loguru import logger
from aocd import get_data
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def is_correct_order(l, r):
    # Both ints
    if type(l) == int and type(r) == int:
        if l == r:
            return -1
        return int(l < r)
    # Both lists
    elif type(l) == list and type(r) == list:
        if len(l) == 0 and len(r) == 0:
            return -1
        if len(l) == 0:
            return 1
        if len(r) == 0:
            return 0
        # Both lists have length > 0, so there are more elements to compare
        next_call = is_correct_order(l[0], r[0])
        # in the end, if both lists have the same length, we can compare the next elements
        if next_call == -1:
            return is_correct_order(l[1:], r[1:])
        return next_call
    # left is int and right is list
    if type(l) == int:
        return is_correct_order([l], r)
    # right is int and left is list
    elif type(r) == int:
        return is_correct_order(l, [r])

def sort_pairs(pairs):
    i = j = 0
    sorted_pairs = []
    while i < len(pairs):
        j = 0
        while j < len(sorted_pairs):
            if is_correct_order(pairs[i], sorted_pairs[j]) == 1:
                sorted_pairs.insert(j, pairs.pop(i))
                break
            j += 1
        if j == len(sorted_pairs):
            sorted_pairs.append(pairs.pop(i))
    return sorted_pairs

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    puzzle_input = puzzle_input.split("\n\n")
    pairs = []
    divider = [[[2]], [[6]]]
    pairs.extend(divider)
    count = 0
    for i, pair in enumerate(puzzle_input, start=1):
        left = eval(pair.split("\n")[0])
        right = eval(pair.split("\n")[1])
        pairs.append(left)
        pairs.append(right)
        if is_correct_order(left, right) == 1:
            count += i
    print(f"Part 1: {count}")
    sorted_pairs = sort_pairs(pairs)
    result_2 = 1
    for i, p in enumerate(sorted_pairs, start=1):
        if p in divider:
            result_2 *= i
    print(f"Part 2: {result_2}")
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
