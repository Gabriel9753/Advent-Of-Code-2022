import sys
from time import time
from tqdm import tqdm
from loguru import logger
import time
from aocd import get_data
# logger.remove()
from copy import deepcopy, copy
logger.add("logging.log", level="INFO")
from collections import defaultdict
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

directions = {(1,0,0), (0,1,0), (-1,0,0), (0,-1,0), (0,0,1), (0,0,-1)}
points = set()
results = defaultdict(int)
targets = defaultdict(int)
min_x = min_y = min_z = 0
max_x = max_y = max_z = 0

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def check_direction(point):
    for direction in directions:
        target = (point[0] + direction[0], point[1] + direction[1], point[2] + direction[2])
        if target not in points:
            results[point] += 1
            
def is_outside(point):
    global min_x, min_y, min_z, max_x, max_y, max_z
    if point[0] < min_x or point[0] > max_x: return True
    if point[1] < min_y or point[1] > max_y: return True
    if point[2] < min_z or point[2] > max_z: return True
    return False

def find_holes():
    global min_x, min_y, min_z, max_x, max_y, max_z
    # Für alle Punkte, die eingeschlossen sind
    points_holes = set()
    points_not_holes = set()
    dfs_steps = 0
    for x in range(min_x+1, max_x):
        for y in range(min_y+1, max_y):
            for z in range(min_z+1, max_z):
                current_point = (x,y,z)
                if current_point in points: continue
                visited = set()
                not_visited = set()
                current_dfs_point = current_point
                while True:
                    dfs_steps += 1
                    visited.add(current_dfs_point)
                    for direction in directions:
                        target = (current_dfs_point[0] + direction[0], current_dfs_point[1] + direction[1], current_dfs_point[2] + direction[2])
                        if target not in points and target not in visited and target not in points_holes:
                            not_visited.add(target)
                    if len(not_visited) == 0:
                        points_holes.update(visited)
                        break
                    current_dfs_point = not_visited.pop()
                    if is_outside(current_dfs_point) or current_dfs_point in points_not_holes:
                        points_not_holes.update(visited)
                        break
    return points_holes
    
def calc_space():
    global min_x, min_y, min_z, max_x, max_y, max_z
    min_x, min_y, min_z = list(points)[0][0], list(points)[0][1], list(points)[0][2]
    max_x, max_y, max_z = list(points)[0][0], list(points)[0][1], list(points)[0][2] 
    for point in points:
        if point[0] < min_x: min_x = point[0]
        if point[1] < min_y: min_y = point[1]
        if point[2] < min_z: min_z = point[2]
        if point[0] > max_x: max_x = point[0]
        if point[1] > max_y: max_y = point[1]
        if point[2] > max_z: max_z = point[2]

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    for line in puzzle_input.splitlines():
        points.add(eval(line.strip().replace("\n", "")))
    for point in points:
        check_direction(point)
    print(f"Part 1: {sum(i for i in results.values())}")
    results.clear()
    calc_space()
    start = time.time()
    points_holes = find_holes()
    print(f"Time: {time.time() - start:.10f}s")
    points.update(points_holes)
    for point in points:
        check_direction(point)
    result_2 = sum(i for i in results.values())
    print(f"Part 2: {result_2}")
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
