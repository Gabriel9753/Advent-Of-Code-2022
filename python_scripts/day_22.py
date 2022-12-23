import sys
from loguru import logger
from aocd import get_data
import time
from collections import defaultdict, deque
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")
from tqdm import tqdm

void = "⬛️"
blocking = "🪵"
way =      "🟩"
up =       "🔼"
right = "▶️"
down = "🔽"
left = "◀️"
walked = "🔸"

CUBE_WIDTH = 0
CUBE_HEIGHT = 0
'''
   ######
   #A##B#
   ######
   ###
   #C#
   ###
######
#E##D#
######
###
#F#
###
'''
CUBES = {
    "A": {
        "V": [(51, 1), (100, 1), (100, 50), (51, 50)],
        # A -> F
        "Up": lambda x: (CUBES["F"]["V"][0][0], CUBES["F"]["V"][0][1] + abs(CUBES["A"]["V"][0][0] - x[0]), 0),
        # A -> E
        "Left": lambda x: (CUBES["E"]["V"][0][0], CUBES["E"]["V"][0][1] + abs(CUBES["A"]["V"][3][1] - x[1]), 0),
    },
    "B": {
        "V": [(101, 1), (150, 1), (150, 50), (101, 50)],
        # B -> F
        "Up": lambda x: (CUBES["F"]["V"][3][0] + abs(CUBES["B"]["V"][0][0] - x[0]), CUBES["F"]["V"][2][1], 3),
        # B -> D
        "Right": lambda x: (CUBES["D"]["V"][2][0], CUBES["D"]["V"][1][1] + abs(CUBES["B"]["V"][2][1] - x[1]), 2),
        # B -> C
        "Down": lambda x: (CUBES["C"]["V"][2][0], CUBES["C"]["V"][1][1] + abs(CUBES["B"]["V"][3][0] - x[0]), 2),
    },
    "C": {
        "V": [(51, 51), (100, 51), (100, 100), (51, 100)],
        # C -> B
        "Right": lambda x: (CUBES["B"]["V"][3][0] + abs(CUBES["C"]["V"][1][1] - x[1]), CUBES["B"]["V"][2][1], 3),
        # C -> E
        "Left": lambda x: (CUBES["E"]["V"][0][0] + abs(CUBES["C"]["V"][0][1] - x[1]), CUBES["E"]["V"][0][1], 1),
    },
    "D": {
        "V": [(51, 101), (100, 101), (100, 150), (51, 150)],
        # D -> B
        "Right": lambda x: (CUBES["B"]["V"][1][0], CUBES["B"]["V"][1][1] + abs(CUBES["D"]["V"][2][1] - x[1]), 2),
        # D -> F
        "Down": lambda x: (CUBES["F"]["V"][1][0], CUBES["F"]["V"][1][1] + abs(CUBES["D"]["V"][3][0] - x[0]), 2),
    },
    "E": {
        "V": [(1, 101), (50, 101), (50, 150), (1, 150)],
        # E -> C
        "Up": lambda x: (CUBES["C"]["V"][0][0], CUBES["C"]["V"][0][1] + abs(CUBES["E"]["V"][0][0] - x[0]), 0),
        # E -> A
        "Left": lambda x: (CUBES["A"]["V"][0][0], CUBES["A"]["V"][0][1] + abs(CUBES["E"]["V"][3][1] - x[1]), 0),
    },
    "F": {
        "V": [(1, 151), (50, 151), (50, 200), (1, 200)],
        # F -> A
        "Left": lambda x: (CUBES["A"]["V"][0][0] + abs(CUBES["F"]["V"][0][1] - x[1]), CUBES["A"]["V"][0][1], 1),
        # F -> B
        "Down": lambda x: (CUBES["B"]["V"][0][0] + abs(CUBES["F"]["V"][3][0] - x[0]), CUBES["B"]["V"][0][1], 1),
        # F -> D
        "Right": lambda x: (CUBES["D"]["V"][3][0] + abs(CUBES["F"]["V"][1][1] - x[1]), CUBES["D"]["V"][3][1], 3),
    },
}

def build_puzzle_map(puzzle_input):
    puzzle_input = puzzle_input.split("\n\n")[0]
    puzzle_map = defaultdict(lambda: void)
    for row, line in enumerate(puzzle_input.splitlines(), start=1):
        for col, char in enumerate(line, start=1):
            if char != " ":
                puzzle_map[(col, row)] = way if char == "." else blocking
    CUBE_WIDTH = max(puzzle_map.keys(), key=lambda x: x[0])[0]/3
    CUBE_HEIGHT = max(puzzle_map.keys(), key=lambda x: x[1])[1]/4
    print(CUBE_WIDTH, CUBE_HEIGHT)
    return puzzle_map

def build_instructions(puzzle_input):
    puzzle_input = puzzle_input.split("\n\n")[1]
    last_char = puzzle_input[-1]
    try:
        int(last_char)
        puzzle_input = "".join([puzzle_input, "X"])
    except ValueError:
        puzzle_input = "".join([puzzle_input, "1"])
    instructions = []
    is_num = True
    while puzzle_input:
        instruction = ""
        for _char in puzzle_input:
            before = is_num
            try:
                _num = int(_char)
                is_num = True
                if before == is_num:
                    instruction = "".join([instruction, _char])
            except ValueError:
                is_num = False
                if before == is_num:
                    instruction = "".join([instruction, _char])
            if before != is_num:
                instructions.append(instruction)
                break
            puzzle_input = puzzle_input[1:]
    for i, instruction in enumerate(instructions):
        try:
            instructions[i] = int(instruction)
        except ValueError:
            pass
    return deque(instructions)

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
    with open("day_22_map.txt", "w", encoding="utf-8") as f:
        f.write(_str)
    if cur_pos:
        puzzle_map[cur_pos] = _temp
    
def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

DIRECTIONS = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1)
}

TURNS = {"R": 1, "L": -1}

def get_start_pos(puzzle_map):
    first_row = [(col, row) for col, row in puzzle_map.keys() if row == 1]
    return first_row[0]

def is_warpable(puzzle_map, pos):
    if puzzle_map[pos] == void:
        return False
    return True

def get_current_cube(current_pos):
    for cube in CUBES:
        if CUBES[cube]["V"][0][0] <= current_pos[0] <= CUBES[cube]["V"][1][0] and CUBES[cube]["V"][0][1] <= current_pos[1] <= CUBES[cube]["V"][3][1]:
            return cube

MOVE_NUM_TO_NAME = {0: "Right", 1: "Down", 2: "Left", 3: "Up"}

def warp(current_pos, current_dir, cube, puzzle_map, part_1=True):
    new_dir = current_dir
    if not part_1:
        _result = cube[MOVE_NUM_TO_NAME[current_dir]](current_pos)
        new_pos = (_result[0], _result[1])
        new_dir = _result[2]
    else:
        if current_dir == 0:
            new_pos = (min(puzzle_map.keys(), key=lambda x: x[0] if (puzzle_map[x] != void and x[1] == current_pos[1]) else 999)[0], current_pos[1])
        elif current_dir == 1:
            new_pos = (current_pos[0], min(puzzle_map.keys(), key=lambda x: x[1] if (puzzle_map[x] != void and x[0] == current_pos[0]) else 999)[1])
        elif current_dir == 2:
            new_pos = (max(puzzle_map.keys(), key=lambda x: x[0] if (puzzle_map[x] != void and x[1] == current_pos[1]) else -999)[0], current_pos[1])
        elif current_dir == 3:
            new_pos = (current_pos[0], max(puzzle_map.keys(), key=lambda x: x[1] if (puzzle_map[x] != void and x[0] == current_pos[0]) else -999)[1])
            
    return new_pos, new_dir

def solve_part(puzzle_map, instructions, part_1=True):
    current_pos = get_start_pos(puzzle_map)
    current_dir = 0
    
    with tqdm(total=len(instructions)) as pbar:
        while instructions:
            instruction = instructions.popleft()
            if isinstance(instruction, str):
                new_dir = (current_dir + TURNS[instruction])
                current_dir = 3 if new_dir < 0 else 0 if new_dir > 3 else new_dir
            else:
                for _ in range(instruction):
                    new_pos = tuple(map(sum, zip(current_pos, DIRECTIONS[current_dir])))
                    if puzzle_map[new_pos] == void:
                        current_cube = get_current_cube(current_pos)
                        warp_pos, warp_dir = warp(current_pos, current_dir, CUBES[current_cube], puzzle_map, part_1)
                        if puzzle_map[warp_pos] == blocking:
                            break
                        puzzle_map[current_pos] = walked
                        current_pos = warp_pos
                        current_dir = warp_dir
                    elif puzzle_map[new_pos] == blocking:
                        break
                    else:
                        puzzle_map[current_pos] = walked
                        current_pos = new_pos
            pbar.update(1)
    print_map(puzzle_map, current_pos)
    return current_pos, current_dir


def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    puzzle_map = build_puzzle_map(puzzle_input)
    instructions = build_instructions(puzzle_input)
    final_pos, final_dir = solve_part(puzzle_map, instructions)
    # print_map(puzzle_map, final_pos)
    print(f"1000 * {final_pos[1]} + 4 * {final_pos[0]} + {final_dir} = {1000 * final_pos[1] + 4 * final_pos[0] + final_dir}")
    puzzle_map = build_puzzle_map(puzzle_input)
    instructions = build_instructions(puzzle_input)
    final_pos, final_dir = solve_part(puzzle_map, instructions, False)
    # print_map(puzzle_map, final_pos)
    print(f"1000 * {final_pos[1]} + 4 * {final_pos[0]} + {final_dir} = {1000 * final_pos[1] + 4 * final_pos[0] + final_dir}")

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
