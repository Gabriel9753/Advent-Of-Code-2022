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

def positions_without_beacons(koordinaten, signal_metas, y=0) -> int:
    positions = []
    for signal_meta in signal_metas:
        signal_edge = signal_meta["edge"]
        edge_1 = None
        edge_2 = None
        for edge in signal_edge:
            if edge[1] == y:
                if edge_1 is None:
                    edge_1 = edge
                else:
                    edge_2 = edge
        # Spitze oben oder unten
        if edge_1 is not None and edge_2 is None:
            positions.append(edge_1)
        elif edge_1 is not None and edge_2 is not None:
            _x1 = edge_1[0]
            _x2 = edge_2[0]
            if _x1 > _x2:
                _x1, _x2 = _x2, _x1
            for _x in range(_x1, _x2 + 1):
                if koordinaten[(_x, y)] != "B" or koordinaten[(_x, y)] != "S":
                    positions.append((_x, y))
    return len(set(positions))

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def found_beacon(koordinaten, coord):
    return koordinaten[coord] == "B"

def mark_koordiaten(koordinaten, coord):
    if koordinaten[coord] == ".":
        koordinaten[coord] = "#"
    return koordinaten
        
def check_beacon_quadrant(sensor, beacon):
    if sensor[0] < beacon[0] and sensor[1] < beacon[1]:
        return 1
    elif sensor[0] > beacon[0] and sensor[1] < beacon[1]:
        return 2
    elif sensor[0] > beacon[0] and sensor[1] > beacon[1]:
        return 3
    elif sensor[0] < beacon[0] and sensor[1] > beacon[1]:
        return 4
    elif sensor[0] == beacon[0] and sensor[1] < beacon[1]:
        return 5
    elif sensor[0] == beacon[0] and sensor[1] > beacon[1]:
        return 6
    elif sensor[0] < beacon[0] and sensor[1] == beacon[1]:
        return 7
    elif sensor[0] > beacon[0] and sensor[1] == beacon[1]:
        return 8

def get_direction_chain(sensor, beacon):
    if check_beacon_quadrant(sensor, beacon) == 1:
        return [(-1, 1), (-1, -1), (1, -1), (1, 1)]
    elif check_beacon_quadrant(sensor, beacon) == 2:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    elif check_beacon_quadrant(sensor, beacon) == 3:
        return [(1, -1), (1, 1), (-1, 1), (-1, -1)]
    elif check_beacon_quadrant(sensor, beacon) == 4:
        return [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    elif check_beacon_quadrant(sensor, beacon) == 5:
        return [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    elif check_beacon_quadrant(sensor, beacon) == 6:
        return [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    elif check_beacon_quadrant(sensor, beacon) == 7:
        return [(-1, 1), (-1, -1), (1, -1), (1, 1)]
    elif check_beacon_quadrant(sensor, beacon) == 8:
        return [(1, -1), (1, 1), (-1, 1), (-1, -1)]

def mark_radius(koordinaten, signal, beacon):
    directions = get_direction_chain(signal, beacon)
    current_position = (beacon[0], beacon[1])
    signal_meta = {
        "signal_pos": signal,
        "beacon_pos": beacon,
        "edge": []
    }
    start_position = current_position
    start_direction = directions[0]
    for direction in directions:
        counter = 1
        while counter == 1 or (current_position[0] != signal[0] and current_position[1] != signal[1]):
            current_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            # koordinaten = mark_koordiaten(koordinaten, current_position)
            signal_meta["edge"].append(current_position)
            counter += 1
    if start_position != current_position:
        while current_position != start_position:
            current_position = (current_position[0] + start_direction[0], current_position[1] + start_direction[1])
            # koordinaten = mark_koordiaten(koordinaten, current_position)
            signal_meta["edge"].append(current_position)
    signal_meta["edge"] = set(signal_meta["edge"])
    return koordinaten, signal_meta

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    koordinaten = defaultdict(lambda: ".")
    sensor_beacon = []
    for line in puzzle_input.splitlines():
        coords = re.findall(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line.replace("\n", "").strip())
        coords = coords[0]
        sensor = (int(coords[0]), int(coords[1]))
        beacon = (int(coords[2]), int(coords[3]))
        koordinaten[sensor] = "S"
        koordinaten[beacon] = "B"
        _sb = {"sensor": sensor, "beacon": beacon}
        sensor_beacon.append(_sb)
        
    signal_metas = []
    for sensor_beacon in tqdm(sensor_beacon):
        koordinaten, signal_meta = mark_radius(koordinaten, sensor_beacon["sensor"], sensor_beacon["beacon"])
        signal_metas.append(signal_meta)
    # matrix = dict_to_matrix(koordinaten)
    # print_matrix(matrix)
    
    print(f'Part 1: {positions_without_beacons(koordinaten, signal_metas, y=10)-1}')
    
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
