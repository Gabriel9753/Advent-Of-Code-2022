import sys
from time import time
from loguru import logger
from aocd import get_data
from tqdm import tqdm
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")
with open(f"python_scripts/day_{day}_2__map.txt", "w") as f:
    f.write("")
    
MIN_X, MAX_X, MIN_Y, MAX_Y = 0, 0, 0, 0
MAP_SPACING = 5

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def norm_coord(x, y):
    return x - MIN_X, y - MIN_Y

def norm_x(x):
    return x - MIN_X
    

def print_map(_map):
    global MIN_X, MAX_X, MIN_Y, MAX_Y
    str_for_file = ""
    # print(f"MIN_X: {MIN_X}, MAX_X: {MAX_X}, MIN_Y: {MIN_Y}, MAX_Y: {MAX_Y}")
    for i in range(MIN_X, MAX_X + 1):
        if i == MAX_X:
            # print(f"{' ' * (MAP_SPACING-3)}{i}")
            str_for_file += f"{' ' * (MAP_SPACING-3)}{i}\n"
        elif i == MIN_X:
            # print(f"{' ' * (MAP_SPACING-1)}{i}", end="")
            str_for_file += f"{' ' * (MAP_SPACING-1)}{i}"
        else:
            # print(f"{' ' * (MAP_SPACING-3)}{i}", end="")
            str_for_file += f"{' ' * (MAP_SPACING-3)}{i}"
    for i, line in enumerate(_map):
        row = str(i) + " " * (MAP_SPACING - len(str(i))) + "    ".join(line)
        str_for_file += row + "\n"
        # print(row)
    with open(f"python_scripts/day_{day}_2__map.txt", "a+") as f:
        f.write(str_for_file + "\n\n")

def build_map():
    _map = []
    
    return _map
class Sand:
    sand_counter = 0
    _map = []
    # 1. down, 2. left-diagonal, 3. right-diagonal 4. Stop
    directions = [(0, 1), (-1, 1), (1, 1)]
    sand_moving_in_abyss = False
    _sand = []
    
    def __init__(self, start_x, start_y):
        Sand.sand_counter += 1
        self.sand_id = Sand.sand_counter
        self.x = start_x
        self.y = start_y
        Sand._map[self.y][self.x] = "+"
        self.stopped = False
        Sand._sand.append(self)
    
    @classmethod
    def all_rested(cls):
        if not cls._sand[-1].stopped:
            return False
        return True
    
    @classmethod
    def move_sand(cls):
        cls._sand[-1].move()
        # for sand in cls._sand:
        #     if not sand.stopped:
        #         sand.move()
    
    def move(self):
        for _dir in self.directions:
            _x = self.x
            _y = self.y
            _x += _dir[0]
            _y += _dir[1]
            if _x < 0 or _x > norm_x(MAX_X) or _y < 0 or _y > MAX_Y:
                Sand._map[self.y][self.x] = "<"
                Sand.sand_moving_in_abyss = True
                self.stopped = True
                self.x = -1
                self.y = -1
                return
            if Sand._map[_y][_x] == ".":
                Sand._map[self.y][self.x] = "."
                self.x = _x
                self.y = _y
                Sand._map[self.y][self.x] = "+"
                return 
        self.stopped = True
        Sand._map[self.y][self.x] = "o"
      
def solve(puzzle_input):
    global MIN_X, MAX_X, MIN_Y, MAX_Y
    logger.info(f"Solving puzzle - day {day}...")
    ground_y = 0
    ground_start_x = 0
    ground_to_x = 0
    x_values = []
    y_values = []
    for line in puzzle_input.splitlines():
        for _c in line.split(" -> "):
            _x = int(_c.split(",")[0])
            _y = int(_c.split(",")[1])
            x_values.append(_x)
            y_values.append(_y)
            
    MIN_X, MAX_X, MIN_Y, MAX_Y = min(x_values), max(x_values), min(y_values), max(y_values)
    ground_y = MAX_Y + 2
    MIN_X -= 400
    MAX_X += 400
    MAX_Y += 2
    y_range = MAX_Y
    x_range = MAX_X - MIN_X
    # build map with all points
    _map = []
    for y in range(y_range + 1):
        _map.append(["."] * (x_range + 1))
        
    for line in puzzle_input.splitlines():
        _stack = line.split(" -> ")
        while len(_stack) > 1:
            _from = _stack.pop(0)
            _to = _stack[0]
            _from_x, _from_y = int(_from.split(",")[0]), int(_from.split(",")[1])
            _to_x, _to_y = int(_to.split(",")[0]), int(_to.split(",")[1])
            if _from_x > _to_x:
                _from_x, _to_x = _to_x, _from_x
            if _from_y > _to_y:
                _from_y, _to_y = _to_y, _from_y
            # No diagonal lines
            if _from_x == _to_x:
                _x = norm_x(_from_x)
                for y in range(_from_y, _to_y + 1):
                    _y = y
                    try:
                        _map[_y][_x] = "#"
                    except IndexError:
                        print(_x, _y)
            elif _from_y == _to_y:
                _y = _from_y
                for x in range(_from_x, _to_x + 1):
                    _x = norm_x(x)
                    try:
                        _map[_y][_x] = "#"
                    except IndexError:
                        print(_x, _y)
        
    for i in range(MIN_X, MAX_X + 1):
        _map[MAX_Y][norm_x(i)] = "#"
    Sand._map = _map
    
    start_x, start_y = norm_x(500), 0
    sand = Sand(start_x, start_y)
    with tqdm(total=99999999) as pbar:
        while Sand._map[start_y][start_x] != "o":
            if Sand.all_rested():
                pbar.update()
                if Sand._map[start_y][start_x] == "o":
                    break
                sand = Sand(start_x, start_y)
            else:
                Sand.move_sand()
    print_map(Sand._map)
    print(len(Sand._sand))
    
            

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
