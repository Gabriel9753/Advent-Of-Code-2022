import sys
from time import time
from loguru import logger
from aocd import get_data
from collections import defaultdict
import re
import matplotlib.pyplot as plt
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

def positions_without_beacons(sensors_meta, y=0) -> int:
    positions = set()
    for sensor_meta in sensors_meta:
        sensor = sensor_meta["sensor_pos"]
        sensor_vertices = sensor_meta["vertices"]
        vertex_u = max(sensor_vertices, key=lambda x: x[1])
        vertex_d = min(sensor_vertices, key=lambda x: x[1])
        if vertex_d[1] <= y <= vertex_u[1]:
            dy = abs(sensor[1] - y)
            dx = (abs(vertex_u[1] - sensor[1]) - dy)
            for x in range(sensor[0] - dx, sensor[0] + dx + 1):
                positions.add((x, y))
    return len(positions)

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
    # -x
    if sensor[0] < beacon[0] and sensor[1] < beacon[1]:
        return 1
    # +x
    elif sensor[0] > beacon[0] and sensor[1] < beacon[1]:
        return 2
    # -x
    elif sensor[0] > beacon[0] and sensor[1] > beacon[1]:
        return 3
    # +x
    elif sensor[0] < beacon[0] and sensor[1] > beacon[1]:
        return 4
    # -x or x
    elif sensor[0] == beacon[0] or sensor[1] == beacon[1]:
        return 5

def calc_m(beacon, sensor):
    if check_beacon_quadrant(sensor, beacon) == 1 or check_beacon_quadrant(sensor, beacon) == 3:
        return -1
    return 1

def calc_c(beacon, m):
    if m == -1:
        return beacon[1] + beacon[0]
    return beacon[1] - beacon[0]

def calc_x1(beacon, sensor, c, m):
    if beacon[1] == sensor[1]:
        return (beacon[0], sensor[1])
    # yS == yX1
    return (m * (sensor[1] - c), sensor[1])

def calc_x2(beacon, sensor, c, m):
    if beacon[0] == sensor[0]:
        return (sensor[0], beacon[1])
    # xS == xX2
    if beacon[1] > sensor[1] and beacon[0] > sensor[0]:
        return (sensor[0], m * (sensor[0] - c))
    elif beacon[1] < sensor[1] and beacon[0] < sensor[0]:
        return (sensor[0], m * (sensor[0] - c))
    return (sensor[0], m * (sensor[0] + c))

def calc_x3(sensor, x1):
    dx = abs(sensor[0] - x1[0])
    if sensor[0] < x1[0]:
        return (sensor[0] - dx, sensor[1])
    return (sensor[0] + dx, sensor[1])

def calc_x4(sensor, x2):
    dy = abs(sensor[1] - x2[1])
    if sensor[1] < x2[1]:
        return (sensor[0], sensor[1] - dy)
    return (sensor[0], sensor[1] + dy)
    
def get_vertices(koordinaten, sensor, beacon):
    m = calc_m(beacon, sensor)
    c = calc_c(beacon, m)
    x1 = calc_x1(beacon, sensor, c, m)
    x2 = calc_x2(beacon, sensor, c, m)
    x3 = calc_x3(sensor, x1)
    x4 = calc_x4(sensor, x2)
    r = abs(x1[0] - sensor[0]) + abs(x1[1] - sensor[1])
    sensor_meta = {
        "sensor_pos": sensor,
        "beacon_pos": beacon,
        "vertices": [x1, x2, x3, x4],
        "r": r,
    }
    # for vertex in sensor_meta["vertices"]:
    #     koordinaten = mark_koordiaten(koordinaten, vertex)

    return koordinaten, sensor_meta

def solve_2(sensors, y):
    ranges = []
    for sensor in sensors:
        sx = sensor["sensor_pos"][0]
        sy = sensor["sensor_pos"][1]
        r = sensor["r"]
        dy = abs(y - sy)
        if dy > r:
            continue
        dx = r - dy
        ranges.append((sx - dx, sx + dx))
    ranges.sort()
    min_x, max_x = ranges[0]
    for x1, x2 in ranges[1:]:
        min_test = min_x - 1
        if x1 < min_test and x2 < min_test:
            return min_test
        max_test = max_x + 1
        if x1 > max_test and x2 > max_test:
            return max_test
        min_x = min(x1, min_x)
        max_x = max(x2, max_x)
    return False

def solve_second(sensors):
    for y in range(4_000_000):
        if x := solve_2(sensors, y):
            print(x, y)
            return x * 4_000_000 + y

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
        
    sensors_meta = []
    # 10
    y = 10
    s_or_b_in_row = set()
    for sensor_beacon in tqdm(sensor_beacon):
        sensor = sensor_beacon["sensor"]
        beacon = sensor_beacon["beacon"]
        if sensor[1] == y:
            s_or_b_in_row.add(sensor)
        elif beacon[1] == y:
            s_or_b_in_row.add(beacon)
        koordinaten, signal_meta = get_vertices(koordinaten, sensor, beacon)
        sensors_meta.append(signal_meta)
    
    # for i in range(-10, 30):
    #     koordinaten[(i, y)] = "~"
    # koordinaten[(14, 11)] = "§"
    # matrix = dict_to_matrix(koordinaten)
    # print_matrix(matrix)
    print(f'Part 1: {positions_without_beacons(sensors_meta, y=y) - len(s_or_b_in_row)}')
    print(f"Part 2: {solve_second(sensors_meta)}")
    
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
