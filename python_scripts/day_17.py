import sys
from time import time
from loguru import logger
from aocd import get_data
import math
from tqdm import tqdm
from collections import defaultdict
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

last_added_stone = set()
solid_squares = set([(x,0) for x in range(7)])
X_START_OFFSET = 2
Y_START_OFFSET = 4
move_pattern = []
move_dict = {"<": (-1, 0), ">": (1, 0)}

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def reset():
    global last_added_stone, solid_squares
    last_added_stone = set()
    solid_squares = set([(x,0) for x in range(7)])

def draw_squares():
    max_y = max([y for _, y in solid_squares])+3
    for y in range(max_y, -1, -1):
        for x in range(7):
            if (x, y) in last_added_stone:
                print("@", end="")
            elif (x, y) in solid_squares:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("\n-----------------\n")

stones = {
    #horizontal
    0: lambda x, y: set([(x, y), (x+1, y), (x+2, y), (x+3, y)]),
    #plus
    1: lambda x, y: set([(x+1, y), (x, y+1), (x+1, y+1), (x+2, y+1), (x+1, y+2)]),
    # letter l
    2: lambda x, y: set([(x, y), (x+1, y), (x+2, y), (x+2, y+1), (x+2, y+2)]),
    # vertical
    3: lambda x, y: set([(x, y), (x, y+1), (x, y+2), (x, y+3)]),
    # block
    4: lambda x, y: set([(x, y), (x+1, y), (x, y+1), (x+1, y+1)])
}

def spawn_stone(which, highest_y):
    return stones[which](X_START_OFFSET, highest_y + Y_START_OFFSET).copy()

def stone_fall(stone):
    new_stone = set()
    for x, y in stone:
        new_stone.add((x, y-1))
    if len(new_stone.intersection(solid_squares)) > 0:
        # stone has hit the ground or another stone
        return stone
    return new_stone

def stone_move(stone, direction):
    new_stone = set()
    min_x, max_x = math.inf, -math.inf
    for x, y in stone:
        dx, dy = x+direction[0], y+direction[1]
        min_x = min(min_x, dx)
        max_x = max(max_x, dx)
        new_stone.add((dx, dy))
    if len(new_stone.intersection(solid_squares)) > 0 or min_x < 0 or max_x > 6:
        # stone has hit the ground or another stone
        return stone
    return new_stone

def search_intervall(key, stone_num, highest_y):
    global cache
    if key in cache:
        last_rock_nr, last_height = cache[key]
        left_rocks = 1_000_000_000_000-stone_num
        intervall_rocks = stone_num - last_rock_nr
        intervall_height = highest_y - last_height
        quotient, r = divmod(left_rocks, intervall_rocks)
        return int(highest_y + intervall_height * quotient) if r == 0 else None
    else:
        cache[key] = stone_num, highest_y

cache = dict()

def simulate(amount_rocks):
    global last_added_stone, cache
    highest_y = 0
    pattern_id = 0
    for stone_num in tqdm(range(amount_rocks)):
        if stone_num == 2022: part_1 = highest_y
        if (part2 := search_intervall((stone_num%5, pattern_id%len(move_pattern)),stone_num,highest_y)):
            return (part_1, part2)
        stone = spawn_stone(stone_num%5, highest_y)
        is_falling = True
        while is_falling:
            stone = stone_move(stone, move_pattern[pattern_id%len(move_pattern)])
            pattern_id += 1
            new_stone = stone_fall(stone)
            if new_stone == stone:
                is_falling = False
                last_added_stone = stone
                solid_squares.update(stone)
                highest_y = max(max([y for _, y in stone]), highest_y)
                amount_rocks -= 1
            else:
                stone = new_stone
    reset()
    return highest_y
    

def solve_part(puzzle_input):
    for c in puzzle_input.strip():
        move_pattern.append(move_dict[c])
    print(simulate(1_000_000_000_000))
    
def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    solve_part(puzzle_input)

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
