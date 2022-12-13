import sys
from time import time
from loguru import logger
from aocd import get_data
import math
from tqdm import tqdm
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

class Graph():
    
    def build_graph_from_matrix(self):
        self.nodes = []
        for i, row in enumerate(self.matrix):
            for j, column in enumerate(row):
                self.nodes.append((i, j))
        
        self.edges = {}
        for node in self.nodes:
            self.edges[node] = {}
            for _dir in DIRECTIONS:
                to_node = (node[0] + _dir[0], node[1] + _dir[1])
                if to_node in self.nodes:
                    edge_value = self.matrix[to_node[0]][to_node[1]] - self.matrix[node[0]][node[1]]
                    # from a to c is not possible
                    if edge_value > 1:
                        continue
                    self.edges[node][to_node] = 1
    
    def dijkstra(self):
        unvisited = {node: None for node in self.nodes} #using None as +inf
        visited = {}
        current = self.start
        currentDistance = 0
        unvisited[current] = currentDistance
        self.shortest_path = {}
        current_steps = 0
        
        while True:
            for neighbour, distance in self.edges[current].items():
                if neighbour not in unvisited: 
                    continue
                newDistance = currentDistance + distance
                if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                    unvisited[neighbour] = newDistance
                    self.shortest_path[neighbour] = current
            visited[current] = currentDistance
            del unvisited[current]
            if not unvisited: 
                break
            candidates = [node for node in unvisited.items() if node[1] is not None]
            try:
                current, currentDistance = min(candidates, key=lambda x: x[1])
            except ValueError:
                break
        self.costs_to_end = visited
    
    def get_path(self, end_node, start_node):
        path = []
        node = end_node
        while node != start_node:
            path.append(node)
            node = self.shortest_path[node]
        path.append(start_node)
        path.reverse()
        return path

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    # print(puzzle_input)
    puzzle_input = puzzle_input.splitlines()
    input_matrix = []
    graph = Graph()
    graph.possible_start_positions = []
    for row in range(len(puzzle_input)):
        _row = []
        for column in range(len(puzzle_input[row])):
            value = puzzle_input[row][column]
            if value == "S":
                graph.start = (row, column)
                value = "a"
            elif value == "E":
                graph.end = (row, column)
                value = "z"
            if value == "a":
                graph.possible_start_positions.append((row, column))
            _row.append(ord(value)-96)
        input_matrix.append(_row)
    graph.matrix = input_matrix
    graph.build_graph_from_matrix()
    graph.dijkstra()
    print(f"Part 1: {len(graph.get_path(graph.end, graph.start))-1}")
    
    cost_for_start = {}
    for _start in tqdm(graph.possible_start_positions, total=len(graph.possible_start_positions)):
        graph.start = _start
        graph.dijkstra()
        try:
            cost_for_start[_start] = len(graph.get_path(graph.end, graph.start))-1
        except KeyError:
            continue
    cost_for_start = sorted(cost_for_start.items(), key=lambda x: x[1])
    print(f"Part 2: {cost_for_start[0][1]} with start position {cost_for_start[0][0]}")
    
    
    
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
