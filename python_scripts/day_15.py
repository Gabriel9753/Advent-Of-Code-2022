import sys
from time import time
from loguru import logger
from aocd import get_data
from collections import defaultdict
import re
from tqdm import tqdm
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def dict_to_matrix(koordinaten):
    x_values = []
    y_values = []
    for key in koordinaten.keys():
        x_values.append(key[0])
        y_values.append(key[1])
    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)
    
    matrix = []
    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            row.append(koordinaten[(x, y)])
        matrix.append(row)
    return matrix
    
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(row))

def positions_without_beacons(koordinaten, y=0) -> int:
    _sum = 0
    for key in koordinaten.keys():
        if key[1] != y:
            continue
        if koordinaten[key] == "⬛️":
            _sum += 1
    return _sum

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def found_beacon(koordinaten, coord):
    return koordinaten[coord] == "📍"

def mark_koordiaten(koordinaten, coord):
    if koordinaten[coord] == "⬜️":
        koordinaten[coord] = "⬛️"
    return koordinaten
        
directions = [(-1,-1), (1,-1), (1,1), (-1,1)]

def mark_radius(koordinaten, start_sensor):
    current_cord = (start_sensor[0], start_sensor[1])
    beacon_found = False
    with tqdm(total=999999999, desc="Marking radius") as pbar:
        while not beacon_found:
            pbar.update(1)
            pbar.set_postfix_str(f"Current cord: {current_cord}")
            _x = current_cord[0]
            _y = current_cord[1] + 1
            current_cord = (_x, _y)
            for _dir in directions:
                scalar = 1
                if not beacon_found:
                    beacon_found = found_beacon(koordinaten, current_cord)
                while scalar == 1 or (current_cord[0] != start_sensor[0] and current_cord[1] != start_sensor[1]):
                    _x = current_cord[0] + _dir[0]
                    _y = current_cord[1] + _dir[1]
                    current_cord = (_x, _y)
                    scalar += 1
                    if not beacon_found:
                        beacon_found = found_beacon(koordinaten, current_cord)
                    koordinaten = mark_koordiaten(koordinaten, current_cord)
    return koordinaten

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    koordinaten = defaultdict(lambda: "⬜️")
    sensor_beacon = []
    for line in puzzle_input.splitlines():
        coords = re.findall(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line.replace("\n", "").strip())
        coords = coords[0]
        sensor = (int(coords[0]), int(coords[1]))
        beacon = (int(coords[2]), int(coords[3]))
        koordinaten[sensor] = "🚦"
        koordinaten[beacon] = "📍"
        _sb = {"sensor": sensor, "beacon": beacon}
        sensor_beacon.append(_sb)
    sensors = [key for key in koordinaten.keys() if koordinaten[key] == "🚦"]
    for sensor in tqdm(sensors):
        koordinaten = mark_radius(koordinaten, sensor)
    koordinaten[(14, 11)] = "🥝"
    koordinaten[(0,0)] = "🍎"
    koordinaten[(0, 20)] = "🍎"
    koordinaten[(20, 0)] = "🍎"
    koordinaten[(20, 20)] = "🍎"
    matrix = dict_to_matrix(koordinaten)
    print_matrix(matrix)
    
    print(f'Part 1: {positions_without_beacons(koordinaten, y=2000000)}')
    
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
