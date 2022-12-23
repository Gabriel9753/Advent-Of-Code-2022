import sys
from loguru import logger
from collections import defaultdict, deque
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")
from tqdm import tqdm
void = "-"

DIRECTIONS = {
    "N": (0,-1),
    "E": (1,0),
    "S": (0,1),
    "W": (-1,0),
    "NE": (1,-1),
    "NW": (-1,-1),
    "SE": (1,1),
    "SW": (-1,1)
}

prios = [(["N", "NE", "NW"], "N"), (["S", "SE", "SW"], "S"), (["W", "NW", "SW"], "W"), (["E", "NE", "SE"], "E")]

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()
    
def print_map(puzzle_map, cur_pos=None):
    if cur_pos:
        _temp = puzzle_map[cur_pos]
        puzzle_map[cur_pos] = "⛔️"
    max_x, max_y = max(puzzle_map.keys(), key=lambda x: x[0])[0], max(puzzle_map.keys(), key=lambda x: x[1])[1]
    min_x, min_y = min(puzzle_map.keys(), key=lambda x: x[0])[0], min(puzzle_map.keys(), key=lambda x: x[1])[1]
    _map = [[puzzle_map[(x, y)] for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)]
    _str = ""
    for row in _map:
        _str = "".join([_str, " ".join(row), "\n"])
    # print(_str)
    _str = _str.replace("#", "🟢").replace(".", "⬜️").replace("-", "⬛️")
    with open("day_23_map.txt", "w", encoding="utf-8") as f:
        f.write(_str)
    if cur_pos:
        puzzle_map[cur_pos] = _temp

def calc_free(puzzle_map):
    free = 0
    min_x, max_x = min(puzzle_map.keys(), key=lambda x: x[0] if puzzle_map[x] == "#" else 9999999)[0], max(puzzle_map.keys(), key=lambda x: x[0] if puzzle_map[x] == "#" else -9999999)[0]
    min_y, max_y = min(puzzle_map.keys(), key=lambda x: x[1] if puzzle_map[x] == "#" else 9999999)[1], max(puzzle_map.keys(), key=lambda x: x[1] if puzzle_map[x] == "#" else -9999999)[1]
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if puzzle_map[(x, y)] != "#":
                free += 1
    return free

def generator():
    while True:
        yield

def solve_part(puzzle_map, elves):
    _round = 1
    result_1 = 0
    for _ in tqdm(generator()):
        # if _round % 7 == 0:
        #     print_map(puzzle_map)
        # time.sleep(0.02)
        if _round == 10:
            result_1 = calc_free(puzzle_map)
        possible_moves = []
        ctr_not_moved = 0
        for elve_id, elve in enumerate(elves):
            e_x, e_y = elve
            
            # 1. check all 8 directions for blocking
            found_elves = []
            for _dir in DIRECTIONS.values():
                dx, dy = e_x+_dir[0], e_y+_dir[1]
                if puzzle_map[(dx, dy)] == '#':
                    found_elves.append((dx, dy))
                    break
            if len(found_elves) == 0:
                ctr_not_moved += 1
                continue
            
            # 2. check the moves in prio order and vote per elve
            for prio_move in prios:
                _dirs = prio_move[0]
                target_dir = prio_move[1]
                ctr_free = 0
                for _dir in _dirs:
                    dx, dy = e_x+DIRECTIONS[_dir][0], e_y+DIRECTIONS[_dir][1]
                    if puzzle_map[(dx, dy)] != '#':
                        ctr_free += 1
                if ctr_free == 3:
                    possible_moves.append((elve_id, (e_x+DIRECTIONS[target_dir][0], e_y+DIRECTIONS[target_dir][1])))
                    break
        
        if ctr_not_moved == len(elves):
            return puzzle_map, result_1, _round
        
        # 3. move the elves if at least one elve voted
        if len(possible_moves) == 0:
            continue
        
        queue = deque(sorted(possible_moves, key=lambda x: x[1]))
        voted_moves = []
        while queue:
            _next = queue.popleft()
            _duplicate = False
            while queue and _next[1] == queue[0][1]:
                _duplicate = True
                queue.popleft()
            if _duplicate: continue
            voted_moves.append(_next)
        
        for voted_move in voted_moves:
            elve_id, move = voted_move
            e_x, e_y = elves[elve_id]
            puzzle_map[(e_x, e_y)] = '.'
            puzzle_map[move] = '#'
            elves[elve_id] = move
            
        # first_considered to end
        prios.append(prios.pop(0))
        _round += 1
        

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    puzzle_map = defaultdict(lambda: '-')
    elves = []
    for y, line in enumerate(puzzle_input.splitlines()):
        for x, char in enumerate(line):
            puzzle_map[(x, y)] = char
            if char == "#":
                elves.append((x, y))
    puzzle_map_1, result_1, _round = solve_part(puzzle_map, elves)
    print_map(puzzle_map_1)
    print(f"Part 1: {result_1} | Part 2: {_round}")

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
