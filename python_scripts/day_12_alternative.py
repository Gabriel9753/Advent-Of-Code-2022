import sys
from time import time
from loguru import logger
from aocd import get_data
import math
from collections import defaultdict, deque
from tqdm import tqdm
# logger.remove()
logger.add("logging.log", level="INFO")

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
Graph = {}

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def dfs(start, end):
    queue = deque([(start, 0)])
    visited = set()
    
    while queue:
        node, steps = queue.popleft()
        if node == end:
            return steps
        if (node, steps) in visited: continue
        visited.add((node, steps))
        for _dir in DIRECTIONS:
            to_node = (node[0] + _dir[0], node[1] + _dir[1])
            if (target := Graph.get(to_node)) is not None:
                distance = target - Graph[node]
                if distance > 1:
                    continue
                elif distance <= 1:
                    queue.append((to_node, steps+1))

def solve(puzzle_input):
    print(puzzle_input)
    start: tuple
    end: tuple
    for row, line in enumerate(puzzle_input.splitlines()):
        for col, char in enumerate(line):
            if char == "S":
                start = (row, col)
            elif char == "E":
                end = (row, col)
            Graph[(row, col)] = ord(char)-97 if (char != "S" and char != "E") else ord("a")-97 if char != "E" else ord("z")-97
            
    print(dfs(start, end))
    
    # get int value of char
    # ord("a") = 97
        
if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_12.txt"))