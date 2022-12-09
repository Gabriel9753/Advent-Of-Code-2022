import sys
from time import time
from loguru import logger
from aocd import get_data
import regex as re
# logger.remove()
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
        self.map = [[" . " for _ in range(size_x)] for _ in range(size_y)]
        self.head = None
        self.knots = []
        self.tail = None
        with open("day_9_map.txt", "w") as f:
            f.write("")
    def __str__(self) -> str:
        # print map beatifully
        map_str = ""
        self.map[self.head.y][self.head.x] = " H "
        self.map[self.tail.y][self.tail.x] = " T "
        for i, knot in enumerate(self.knots):
            self.map[knot.y][knot.x] = f" {i} "
        
        # mark visited positions by tail
        for position in self.tail.visited:
            self.map[position[1]][position[0]] = " # "
        self.map[self.start[1]][self.start[0]] = " S "
        
        for row in self.map:
            map_str += "".join(row) + "\n"
        self.map = [[" . " for _ in range(self.size_x)] for _ in range(self.size_y)]
        return map_str + "\n\n--------------------------------------------------------------------\n\n"
    
    def map_to_file(self):
        with open("day_9_map.txt", "a") as f:
            f.write(str(self))

class Knot:
    def __init__(self, head=None, number=0, pre_knot=None, start_x=0, start_y=0) -> None:
        self.pre_knot = pre_knot
        self.x = start_x
        self.y = start_y
        self.visited = [(self.x, self.y)]
        self.head = head
        self.move_history = []
        self.last_move_type = None
        
    def move_to_predecessor(self):
        pre_knot = self.pre_knot
        # only move if distance >= 2
        if self.calculate_distance(pre_knot)["distance"] >= 2:
            if len(pre_knot.move_history) > 0:
                last_move_head = pre_knot.move_history[-1]
                if last_move_head == "U":
                    self.y = pre_knot.y - 1
                    self.x = pre_knot.x
                elif last_move_head == "D":
                    self.y = pre_knot.y + 1
                    self.x = pre_knot.x
                elif last_move_head == "L":
                    self.x = pre_knot.x + 1
                    self.y = pre_knot.y
                elif last_move_head == "R":
                    self.x = pre_knot.x - 1
                    self.y = pre_knot.y
                else:
                    self.x = pre_knot.x
                    self.y = pre_knot.y
            self.move_history.append(last_move_head)   
            self.visited.append((self.x, self.y))
                
    def calculate_distance(self, knot):
        # calculate distance from head to tail
        # return distance
        distance_dict = {}
        distance_x = abs(knot.x - self.x)
        distance_y = abs(knot.y - self.y)
        
        # distance_x == 1 and distance_y == 1 means that the head is diagonal to the tail
        if distance_x == 1 and distance_y == 1:
            distance_dict = {"distance": 1, "direction": "straight"}
        elif distance_x == 1 and distance_y == 2 or distance_x == 2 and distance_y == 1:
            distance_dict = {"distance": distance_x + distance_y, "direction": "diagonal"}
        else:
            distance_dict = {"distance": distance_x + distance_y, "direction": "straight"}
        return distance_dict
    
    def head_move(self, direction):
        self.move_history.append(direction)
        self.x += MOVE_DICT[direction][0]
        self.y += MOVE_DICT[direction][1]

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    head = Knot()
    knot = Knot(head=head, pre_knot=head)
    for move_instruction in puzzle_input.split("\n"):
        move = move_instruction.strip()[0].upper()
        move_amount = int(re.findall(r"\d+", move_instruction.strip())[0])
        for _ in range(move_amount):
            head.head_move(move)
            knot.move_to_predecessor()
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
