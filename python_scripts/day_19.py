import re
import sys
from time import time
from loguru import logger
from aocd import get_data
from collections import deque
from tqdm import tqdm
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

blueprints = {}

def max_robots_needed(blueprint):
    # 0 ore robots, 1 clay robots, 2 obsidian robots
    _max = {}
    max_ore_robots = max(blueprint["ore_robot"], blueprint["clay_robot"], blueprint["obsidian_robot"][0], blueprint["geode_robot"][0])
    max_clay_robots = blueprint["obsidian_robot"][1]
    max_obsidian_robots = blueprint["geode_robot"][1]
    _max["ore_robots"] = max_ore_robots
    _max["clay_robots"] = max_clay_robots
    _max["obsidian_robots"] = max_obsidian_robots
    return _max
    
def search_max_geodes(blueprint_id, max_time):
    blueprint = blueprints[blueprint_id]
    max_robots = max_robots_needed(blueprint)
    _max = 0
    # 0 ore robot, 1 clay robot, 2 obsidian robot, 3 geode robot
    # 4 current ore, 5 current clay, 6 current obsidian, 7 current geode
    # 8 current time stamp
    # 9 built ore robots, 10 built clay robots, 11 built obsidian robots, 12 built geode robots
    start = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    max_time = max_time
    queue = deque([start])
    visited = set()
    while queue:
        popped_item = queue.pop()
        ore_robots, clay_robots, obsidian_robots, geode_robots, ores, clays, obsidians, geodes, _time, built_ore, built_clay, built_obs, built_geode = popped_item
        if _time == max_time:
            _max = max(_max, geodes)
            continue
        delta_time = max_time-_time
        possible_geode_robots = int(delta_time/2)
        if tuple(popped_item) in visited:
            continue
        visited.add(tuple(popped_item))
        if geodes + delta_time * (geode_robots + possible_geode_robots) < _max:
            continue
        ore_robot_costs, clay_robot_costs, obsidian_robot_costs, geode_robot_costs = blueprint["ore_robot"], blueprint["clay_robot"], blueprint["obsidian_robot"], blueprint["geode_robot"]
        
        _ores = ores + ore_robots
        _clays = clays + clay_robots
        _obsidians = obsidians + obsidian_robots
        _geodes = geodes + geode_robots
        
        if ore_robots <= max_robots["ore_robots"] and _ores >= ore_robot_costs:
            queue.append((ore_robots+built_ore, clay_robots+built_clay, obsidian_robots+built_obs, geode_robots+built_geode, _ores-ore_robot_costs, _clays, _obsidians, _geodes, _time+1, 1, 0, 0, 0))
        if clay_robots <= max_robots["clay_robots"] and _ores >= clay_robot_costs and _clays < obsidian_robot_costs[1]:
            queue.append((ore_robots+built_ore, clay_robots+built_clay, obsidian_robots+built_obs, geode_robots+built_geode, _ores-clay_robot_costs, _clays, _obsidians, _geodes, _time+1, 0, 1, 0, 0))
        if obsidian_robots <= max_robots["obsidian_robots"] and (_ores >= obsidian_robot_costs[0] and _clays >= obsidian_robot_costs[1]):
            queue.append((ore_robots+built_ore, clay_robots+built_clay, obsidian_robots+built_obs, geode_robots+built_geode, _ores-obsidian_robot_costs[0], _clays-obsidian_robot_costs[1], _obsidians, _geodes, _time+1, 0, 0, 1, 0))
        if _ores >= geode_robot_costs[0] and _obsidians >= geode_robot_costs[1]:
            queue.append((ore_robots+built_ore, clay_robots+built_clay, obsidian_robots+built_obs, geode_robots+built_geode, _ores-geode_robot_costs[0], _clays, _obsidians-geode_robot_costs[1], _geodes, _time+1, 0, 0, 0, 1))
        
        queue.append((ore_robots+built_ore, clay_robots+built_clay, obsidian_robots+built_obs, geode_robots+built_geode, _ores, _clays, _obsidians, _geodes, _time+1, 0, 0, 0, 0))
            
    return _max

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    blueprints_raw = puzzle_input.strip().split('Blueprint')
    for i, blueprint_raw in enumerate(blueprints_raw[1:], start=1):
        blueprint = {}
        ore_costs = re.findall(r'.* (\d+) ore.*', blueprint_raw)
        blueprint["ore_robot"] = (int(ore_costs[0]))
        blueprint["clay_robot"] = (int(ore_costs[1]))
        clay_costs = re.findall(r'.* (\d+) clay.*', blueprint_raw)[0]
        blueprint["obsidian_robot"] = (int(ore_costs[2]), int(clay_costs))
        obsidian_costs = re.findall(r'.* (\d+) obsidian.*', blueprint_raw)[0]
        blueprint["geode_robot"] = (int(ore_costs[3]), int(obsidian_costs))
        blueprints[i] = blueprint
    print(blueprints)
    
    # for k in tqdm(blueprints.keys()):
    #     max_geodes = search_max_geodes(k, 24)
    #     blueprints[k]["max_geodes"] = k * max_geodes
    # result_1 = sum([blueprint["max_geodes"] for blueprint in blueprints.values()])
    # print(f"Result 1: {result_1}")
    
    for k in tqdm(blueprints.keys()):
        max_geodes = search_max_geodes(k, 32)
        blueprints[k]["max_geodes"] = max_geodes
    result_2 = [blueprint["max_geodes"] for blueprint in blueprints.values()]
    r_2 = 1
    for r in result_2:
        r_2 *= r
        print(r)
    print(f"Result 2: {r_2}")
    

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}_2.txt"))
