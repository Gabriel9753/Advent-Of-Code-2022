import sys
from time import time
from loguru import logger
from aocd import get_data
from collections import defaultdict
import math
logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def search_part_1(grid, visibles, iter_x, iter_y, vertical=True):
    visible = []
    for x in iter_x:
        current_tallest = -1
        for y in iter_y:
            _x, _y = (y, x) if vertical else (x, y)
            if (tree_height := grid[_x][_y]) > current_tallest:
                current_tallest = tree_height
                visible.append((_y, _x))
            if tree_height >= 9: break
    return visibles + visible

def calc_score_from_point(grid, grid_x, grid_y, x, y):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    scores_per_direction = defaultdict(int)
    current_height = grid[x][y]
    for direction in directions:
        for i in range(1, max(grid_x, grid_y)):
            _x = x + direction[0] * i
            _y = y + direction[1] * i
            if _x < 0 or _x >= grid_x or _y < 0 or _y >= grid_y:
                break
            tree_height = grid[_x][_y]
            if tree_height < current_height:
                scores_per_direction[direction] += 1
            else:
                scores_per_direction[direction] += 1
                break

    score = math.prod(scores_per_direction.values())
    return score

def search_part_2(grid, grid_x, grid_y):
    scores = {}
    for x in range(grid_x):
        for y in range(grid_y):
            if x == 0 or x == grid_x-1 or y == 0 or y == grid_y-1:
                scores[(x, y)] = 0
                continue
            score = calc_score_from_point(grid, grid_x, grid_y, x, y)
            scores[(x, y)] = score
    return max(scores.values())
            
def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    grid = [[int(i) for i in line] for line in puzzle_input.splitlines()]
    grid_x = len(grid[0])
    grid_y = len(grid)
    visibles = []
    visibles = search_part_1(grid, visibles, range(grid_x), range(grid_y))
    visibles = search_part_1(grid, visibles, range(grid_x), range(grid_y-1, -1, -1))
    visibles = search_part_1(grid, visibles, range(grid_y), range(grid_x), vertical=False)
    visibles = search_part_1(grid, visibles, range(grid_y), range(grid_x-1, -1, -1), vertical=False)
    logger.info(f"Solution Part 1: {len(set(visibles))}")
    logger.info(f"Solution Part 2: {search_part_2(grid, grid_x, grid_y)}")            

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
