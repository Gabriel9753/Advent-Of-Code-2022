import sys
from time import time
from loguru import logger
from aocd import get_data
import regex as re
import math
logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

MOVE_DICT = {
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
    "R": (1, 0),
}

class Map:
    def __init__(self, size_x, size_y) -> None:
        self.size_x = size_x
        self.size_y = size_y
        self.start = (size_x//2, size_y//2)
        self.map = [["." for _ in range(size_x)] for _ in range(size_y)]
        self.head = None
        self.knots = []
        self.tail = None
        with open("day_9_map.txt", "w") as f:
            f.write("")
    def __str__(self) -> str:
        # print map beatifully
        map_str = ""
        for i, knot in enumerate(self.knots):
            self.map[knot.y][knot.x] = f"{i+1}"
        
        # mark visited positions by tail
        for position in self.tail.visited:
            self.map[position[1]][position[0]] = "#"
        self.map[self.head.y][self.head.x] = "H"
        self.map[self.tail.y][self.tail.x] = "T"
        self.map[self.start[1]][self.start[0]] = "s"
        
        for row in self.map:
            map_str += "".join(row) + "\n"
        self.map = [["." for _ in range(self.size_x)] for _ in range(self.size_y)]
        return map_str + "\n\n--------------------------------------------------------------------\n\n"
    
    def map_to_file(self):
        with open("day_9_map.txt", "a") as f:
            f.write(str(self))

class Knot:
    def __init__(self, head=None, pre_knot=None, start_x=0, start_y=0) -> None:
        self.pre_knot = pre_knot
        self.x = start_x
        self.y = start_y
        self.visited = [(self.x, self.y)]
        self.head = head
        self.move_directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
    def move_to_predecessor(self):
        predecessor = self.pre_knot
        if self.calculate_distance(predecessor) >= 2:
            self.move()
    
    def move(self):
        predecessor = self.pre_knot
        for _dir in self.move_directions:
            tmp_x, tmp_y = self.x, self.y
            self.x, self.y = tmp_x + _dir[0], tmp_y + _dir[1]
            if self.calculate_distance(predecessor) == 1:
                return
            self.x, self.y = tmp_x, tmp_y
        for _dir in self.move_directions:
            tmp_x, tmp_y = self.x, self.y
            self.x, self.y = tmp_x + _dir[0], tmp_y + _dir[1]
            if self.calculate_distance(predecessor) < 2:
                return
            self.x, self.y = tmp_x, tmp_y
        
    
    def calculate_distance(self, knot):
        d_x = abs(self.x - knot.x)
        d_y = abs(self.y - knot.y)
        return math.sqrt(d_x**2 + d_y**2)
    def head_move(self, direction):
        self.x += MOVE_DICT[direction][0]
        self.y += MOVE_DICT[direction][1]

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def calc_map_size(puzzle_input):
    x, y = 0, 0
    for direction in puzzle_input.split("\n"):
        _dir = direction.split()[0]
        amount = int(direction.split()[1])
        for _ in range(amount):
            x, y = x + MOVE_DICT[_dir][0], y + MOVE_DICT[_dir][1]
    return x, y

def simulate(puzzle_input, amount_knots):
    if amount_knots < 2:
        raise ValueError("Amount of knots must be greater than 2")
    map_x, map_y = 1000, 1000
    # _map = Map(map_x, map_y)
    head = Knot(start_x=map_x//2, start_y=map_y//2)
    knot = Knot(head=head, pre_knot=head, start_x=map_x//2, start_y=map_y//2)
    knots = [knot]
    if amount_knots > 2: 
        for _ in range(amount_knots-2):
            knot = Knot(head=head, pre_knot=knots[-1], start_x=map_x//2, start_y=map_y//2)
            knots.append(knot)
    # _map.head = head
    # _map.knots = knots[:-1]
    # _map.tail = knots[-1]
    for direction in puzzle_input.split("\n"):
        _dir = direction.split()[0]
        amount = int(direction.split()[1])
        for _ in range(amount):
            head.head_move(_dir)
            for knot in knots:
                knot.move_to_predecessor()
                knot.visited.append((knot.x, knot.y))
        # _map.map_to_file()
    return knots

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    knots = simulate(puzzle_input, 2)
    logger.info(f"Part 1: {len(set(knots[-1].visited))}")
    knots = simulate(puzzle_input, 10)
    logger.info(f"Part 2: {len(set(knots[-1].visited))}")
                
if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))
