import sys
import time
from collections import deque
import math

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

_map = set()
_cache = {}

blizzard_types = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1)
}

class Blizzard:
    width = 0
    height = 0
    def __init__(self, start_pos, move):
        self.pos = start_pos
        self.start_pos = (start_pos[0]-1, start_pos[1]-1)
        self.move_type = move
        
    def calc_move(self, _time):
        dx = self.start_pos[0] + _time * self.move_type[0]
        dy = self.start_pos[1] + _time * self.move_type[1]
        if dx < 0:
            dx = (Blizzard.width - abs(dx)) % Blizzard.width
        elif dx >= Blizzard.width:
            dx = dx % Blizzard.width
        if dy < 0:
            dy = (Blizzard.height - abs(dy)) % Blizzard.height
        elif dy >= Blizzard.height:
            dy = dy % Blizzard.height
        return (dx+1, dy+1)
    
    @classmethod
    def get_blizzards(cls, _time):
        return set([blizz.calc_move(_time) for blizz in cls.blizzards])

def is_optimizable(start_pos, end_pos, _time, best_time):
    if get_distance(start_pos, end_pos) + _time < best_time:
        return True
    return False

def get_distance(start_pos, end_pos):
    dx, dy = abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])
    return dx + dy

def score_position(start_pos, end_pos, _time):
    return 1/((get_distance(start_pos, end_pos) * _time)+1)

def dfs(start_pos, end_pos, start_time=0):
    move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
    queue = deque([(start_pos, start_time)])
    visited = set()
    best_time = math.inf
    time_depth = start_time
    while queue:
        current_pos, _time = queue.popleft()
            
        if _time > time_depth:
            time_depth = _time
            queue = deque(sorted(queue, key=lambda x: score_position(x[0], end_pos, x[1]), reverse=True))
            queue = deque(list(queue)[:250])
            
        if current_pos == end_pos:
            best_time = min(best_time, _time)
            break
        
        if (current_pos, _time) in visited: continue
        
        visited.add((current_pos, _time))
        
        if not is_optimizable(current_pos, end_pos, _time, best_time): continue
        
        blizzard_time = (_time+1) % (Blizzard.width*Blizzard.height)
        current_blizzards = _cache.get(blizzard_time)
        if current_blizzards is None:
            current_blizzards = Blizzard.get_blizzards(blizzard_time)
            _cache[blizzard_time] = current_blizzards
            
        for move in move_directions:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            if new_pos in current_blizzards:
                continue
            if new_pos in _map:
                queue.append((new_pos, _time+1))
                
    return best_time


def solve(puzzle_input):
    start_pos = (1, 0)
    blizzards = []
    for row, line in enumerate(puzzle_input.splitlines()):
        for col, char in enumerate(line):
            # _map[(col, row)] = "#" if char == "#" else "."
            if char != "#":
                _map.add((col, row))
            
            if char in blizzard_types.keys():
                blizz = Blizzard((col, row), blizzard_types[char])
                blizzards.append(blizz)
    Blizzard.width = col - 1
    Blizzard.height = row - 1
    end_pos = (Blizzard.width, Blizzard.height+1)
    Blizzard.blizzards = blizzards
    start_full_time = time.time()
    
    # Part 1
    start_1_time = time.time()
    best_time = dfs(start_pos, end_pos, start_time=0)
    print(f"Part 1: {best_time} in {time.time() - start_1_time:.4f} seconds!")
    
    # Part 2
    start_2_time = time.time()
    best_time_2 = best_time
    start_pos, end_pos = end_pos, start_pos
    for _ in range(2):
        best_time_2 = dfs(start_pos, end_pos, start_time=best_time_2)
        start_pos, end_pos = end_pos, start_pos
        
    print(f"Part 2: {best_time_2} in {time.time() - start_2_time:.4f} seconds!")
    print(f"Total time: {time.time() - start_full_time:.4f} seconds!")
                
if __name__ == '__main__':
    solve(read_file("python_scripts/day_24.txt"))
