import sys
from time import time
from loguru import logger
import re
from collections import deque
import time
from collections import defaultdict

# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

valves = {}
flows = {}
distances = {}
valves_with_flow_about_zero = set()
start_valve = ""

def parse_input(puzzle_input):
    
    for line in puzzle_input.splitlines():
        _line = line.strip()
        match = re.search(r"Valve (\w+) has flow rate=(\d+)", _line)
        valve_name = match.group(1)
        valves[valve_name] = []
        flows[valve_name] = int(match.group(2))
        # Extract the names of the connected valves
        match = re.search(r"tunnels lead to valves (([^)]+))", _line)
        if match:
            connected_valves = match.group(1)
            connected_valves_list = connected_valves.split(", ")
        else:
            match = re.search(r"tunnel leads to valve (\w+)", _line)
            connected_valves_list = [match.group(1)]
            
        valves[valve_name] = connected_valves_list

# -------------------------------------------------------------------------------------------------------------------------

def calc_distance(start, end):
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        current_node, distance = queue.popleft()
        if current_node in visited: continue
        visited.add(current_node)
        if current_node == end:
            return distance
        for neighbour in valves[current_node]:
            queue.append((neighbour, distance + 1))
                    
def calc_distances():
    for valve in valves:
        distances[valve] = {}
        for other_valve in valves:
            if valve == other_valve: continue
            distances[valve][other_valve] = calc_distance(valve, other_valve)
            
def delete_all_valves_with_no_flow(start_valve):
    valves_to_delete = []
    for valve in valves:
        if flows[valve] == 0 and valve != start_valve:
            valves_to_delete.append(valve)
    for valve in valves_to_delete:
        del valves[valve]
        del flows[valve]
        del distances[valve]
        for other_valve in valves:
            del distances[other_valve][valve]
    
    for valve in valves:
        valves[valve] = [v for v in valves.keys() if v != valve]


# -------------------------------------------------------------------------------------------------------------------------

def optimizable_1(current_open_valves, mins_left, current_flow_rate, current_max):
    if mins_left == 0: return True
    
    _possible_flow_rate = sum([flows[ov]*mins_left for ov in current_open_valves if flows[ov] > 0]) + current_flow_rate
    if _possible_flow_rate > current_max:
        return True
    
    left_valves = valves_with_flow_about_zero - set(current_open_valves)
    left_valves = sorted(left_valves, key=lambda x: flows[x], reverse=True)
    i = 1
    for valve in left_valves:
        if mins_left - i <= 0: break
        _possible_flow_rate += flows[valve] * (mins_left - i)
        i += 2
    if _possible_flow_rate >= current_max:
        return True
    
    return False

# Part 1
def part_1(start_valve):
    max_time = 30
    for valve in valves.keys():
        if flows[valve] > 0:
            valves_with_flow_about_zero.add(valve)
    len_valves = len(valves) if flows[start_valve] > 0 else len(valves) - 1
    queue = deque([(start_valve, 0, (), 0, 0)])
    visited = set()
    max_flow = 0
    
    while queue:
        current_node, current_min, currently_open_valves, total_flow_rate, min_before = queue.pop()
        if current_min > 10 and total_flow_rate == 0:
            continue
        if current_min == max_time:
            max_flow = max(max_flow, total_flow_rate)
            continue
        if (currently_open_valves, current_node, current_min) in visited:
            continue
        visited.add((currently_open_valves, current_node, current_min))
        
        flow_rate = total_flow_rate
        
        for open_valve in currently_open_valves:
            flow_rate += flows[open_valve] * (current_min - min_before)
        
        if not optimizable_1(currently_open_valves, (max_time-current_min), flow_rate, max_flow):
            continue
        
        if len(currently_open_valves) == len_valves:
            for open_valve in currently_open_valves:
                flow_rate += flows[open_valve] * (max_time - (current_min + 1))
            max_flow = max(max_flow, flow_rate)
            continue
        
                
        if current_node not in currently_open_valves and flows[current_node] > 0:
            queue.append((current_node, current_min+1, tuple(list(currently_open_valves) + [current_node]), flow_rate, current_min))
        
        for neighbour in valves[current_node]:
            if (distances[current_node][neighbour] + current_min <= max_time):
                queue.append((neighbour, current_min + distances[current_node][neighbour], currently_open_valves, flow_rate, current_min))
        
    return max_flow

def optimizable_2(current_open_valves, mins_left, current_flow_rate, current_max):
    if mins_left == 0: return True
    
    _possible_flow_rate = sum([flows[ov]*mins_left for ov in current_open_valves if flows[ov] > 0]) + current_flow_rate
    if _possible_flow_rate > current_max:
        return True
    
    left_valves = valves_with_flow_about_zero - set(current_open_valves)
    left_valves = sorted(left_valves, key=lambda x: flows[x], reverse=False)
    i = 1
    while left_valves:
        if mins_left - i <= 0: break
        _possible_flow_rate += flows[left_valves.pop()] * (mins_left - i)
        if len(left_valves) == 0: break
        _possible_flow_rate += flows[left_valves.pop()] * (mins_left - i)
        i += 3
    if _possible_flow_rate >= current_max:
        return True
    
    return False

# Part 2
def part_2(start_valve):
    max_time = 26
    for valve in valves.keys():
        if flows[valve] > 0:
            valves_with_flow_about_zero.add(valve)
    len_valves = len([v for v in valves if flows[v] > 0])
    queue = deque([(start_valve, start_valve, 0, (), 0)])
    visited = set()
    max_flow = 0
    
    while queue:
        current_node, elephant_node, current_min, currently_open_valves, total_flow_rate = queue.pop()
        if current_min > 4 and total_flow_rate == 0:
            continue
        if current_min == max_time:
            max_flow = max(max_flow, total_flow_rate)
            continue
        if (currently_open_valves, current_node, elephant_node, current_min) in visited:
            continue
        visited.add((currently_open_valves, current_node, elephant_node, current_min))
        
        flow_rate = total_flow_rate
        for open_valve in currently_open_valves:
            flow_rate += flows[open_valve]
            
        if not optimizable_2(currently_open_valves, (max_time-current_min), flow_rate, max_flow):
            continue
        
        if len(currently_open_valves) == len_valves:
            for open_valve in currently_open_valves:
                flow_rate += flows[open_valve] * (max_time - (current_min + 1))
            max_flow = max(max_flow, flow_rate)
            continue
        
        if current_node == elephant_node:
            if current_node not in currently_open_valves and flows[current_node] > 0:
                for e_neighbour in valves[elephant_node]:
                    queue.append((current_node, e_neighbour, current_min+1, tuple(list(currently_open_valves) + [current_node]), flow_rate))
        else:
            if current_node not in currently_open_valves and flows[current_node] > 0 and elephant_node not in currently_open_valves and flows[elephant_node] > 0:
                queue.append((current_node, elephant_node, current_min+1, tuple(list(currently_open_valves) + [current_node, elephant_node]), flow_rate))
            elif current_node not in currently_open_valves and flows[current_node] > 0:
                for e_neighbour in valves[elephant_node]:
                    queue.append((current_node, e_neighbour, current_min+1, tuple(list(currently_open_valves) + [current_node]), flow_rate))
            elif elephant_node not in currently_open_valves and flows[elephant_node] > 0:
                for c_neighbour in valves[current_node]:
                    queue.append((c_neighbour, elephant_node, current_min+1, tuple(list(currently_open_valves) + [elephant_node]), flow_rate))
        
        for c_neighbour in valves[current_node]:
            for e_neighbour in valves[elephant_node]:
                queue.append((c_neighbour, e_neighbour, current_min + 1, currently_open_valves, flow_rate))
            
    return max_flow

def solve(puzzle_input):
    global VALVES, FLOWS, distances
    logger.info(f"Solving puzzle - day {day}...")
    parse_input(puzzle_input)
    start_valve = "AA"
    # calc_distances()
    # delete_all_valves_with_no_flow(start_valve)
    # start = time.time()
    # part_1_result = part_1(start_valve)
    # print(f"Part 1: {part_1_result}")
    # print(f"Time: {time.time() - start:.4f}")
    
    cache_distance = distances
    distances = defaultdict(dict)
    for k, v in cache_distance.items():
        for k2, v2 in v.items():
            if v2 == 1:
                distances[k][k2] = 1
    
    start = time.time()
    part_2_result = part_2(start_valve)
    print(f"Part 2: {part_2_result}")
    print(f"Time: {time.time() - start:.4f}")
    
if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))
