# Created: 2022-12-07
# Author: https://github.com/Gabriel9753
# Description: Day 7 of the Advent of Code 2022
# avg time to run: ~0.002s
import sys
from time import time
import regex as re
from typing import List
from loguru import logger
logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

PART_1 = 100000
PART_2 = 30000000

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

class File_System:
    """
        File System class to store all nodes and
        calculate the total size of the file system.
    """
    def __init__(self, name: str, root_node, max_size: int) -> None:
        self.name: str = name
        self.root_node: Node = root_node
        self.total_size: int = 0
        self.max_size: int = max_size
        self.nodes: List[Node] = [root_node]
        self.dirs: List[Node] = [root_node]
        self.files: List[Node] = []

    def add_node(self, node):
        """ Add a node to the file system. """
        self.nodes.append(node)
        self.dirs.append(node) if node.is_dir else self.files.append(node)
    
    def calc_size(self):
        """ Calculate the total size of the file system. """
        self.total_size = self.calc_fs_size(self.root_node)
    
    def calc_fs_size(self, node):
        """ Calculate the size of a node and all its children recursively. """
        if node.is_file:
            return node.size
        else:
            node.size = \
                sum([self.calc_fs_size(child) for child in node.children])
            return node.size
    
    def delete_node(self, node):
        """ Delete a node from the file system recursively. """
        self.nodes.remove(node)
        self.dirs.remove(node) if node.is_dir else self.files.remove(node)
        node.parent.children.remove(node)
        for child in node.children:
            self.delete_node(child)
        del node
        
    def delete_fs_node(self, node):
        """ Delete a node from the file system and update the total size. """
        self.delete_node(node)
        self.calc_size()
    
    def print_recursive(self, node):
        """ Print the file system recursively. """
        indentation = len(node.path.split("/")) - 1
        print(f"| {'    ' * indentation}--- {node}")
        for child in node.children:
            self.print_recursive(child)
    
    def print_fs(self):
        """ Print the file system. """
        print(f"{'-' * 30} {self.name} {'-' * 30}")
        # information about the file system
        print(f"| Total size: {self.total_size} bytes")
        print(f"| Number of nodes: {len(self.nodes)}")
        print(f"| Number of directories: {len(self.dirs)}")
        print(f"| Number of files: {len(self.files)}")
        print(f"| Max size: {self.max_size} bytes")
        print(f"| Free space: {self.max_size - self.total_size} bytes")
        print("| File system:\n|")
        self.print_recursive(self.root_node)
        print(f"{'-' * (30 + len(self.name))}--{'-' * 30}")

    def delete_dir_for_update(self, update_size):
        """
            Delete the smallest possible directory to make space for an update.
        """
        _free = self.max_size - self.total_size
        required_space = update_size - _free
        possible_dirs = [d for d in self.dirs if d.size >= required_space]
        dir_to_delete = min(possible_dirs, key=lambda d: d.size)
        dir_to_delete_size = dir_to_delete.size

        if dir_to_delete == self.root_node:
            raise Exception("Cannot delete root node.")
        self.delete_fs_node(dir_to_delete)
        return dir_to_delete_size

class Node:
    """ Node class to store the name, size, parent, children, and type of a node. """
    def __init__(self, name: str, size: int=0, parent=None, is_file: bool=False):
        self.name: str = name
        self.path: str = f"{parent.path}/{name}" if parent else name
        self.children: List[Node] = []
        self.parent: Node = parent
        self.size: int = size
        self.is_file: bool = is_file
        self.is_dir: bool = not is_file

    def __str__(self) -> str:
        return f'{self.name} ({"file" if self.is_file else "dir"}, {self.size} bytes)'

def parse_input_to_fs(puzzle_input):
    """ Parse the input to a file system. """
    lines = [l.strip() for l in puzzle_input.splitlines()]
    current_node = Node("root")
    fs = File_System("AOC2022:", current_node, max_size=70000000)
    for line in lines:
        if line.startswith("$ ls"):
            continue
        elif line.startswith("$ cd"):
            if line == "$ cd ..":
                current_node = current_node.parent
            elif line == "$ cd /":
                continue
            else:
                node_name = re.search(r"\$ cd (.+)", line).group(1)
                current_node = [n for n in current_node.children if n.name == node_name][0]
        elif line.startswith("dir"):
            new_node = re.search(r"dir (.+)", line).group(1)
            new_node = Node(name=new_node, parent=current_node)
            fs.add_node(new_node)
            current_node.children.append(new_node)
        # default case is a file
        else:
            if line[0].isdigit():
                _size = int(re.search(r"(\d+) (.+)", line).group(1))
                _name = re.search(r"(\d+) (.+)", line).group(2)
                new_node = Node(_name, size=_size, parent=current_node, is_file=True)
                current_node.children.append(new_node)
                fs.add_node(new_node)
    return fs

def solve(puzzle_input):
    '''Solves the puzzle'''
    logger.info(f"Solving puzzle from day {day}...")
    fs = parse_input_to_fs(puzzle_input)
    fs.calc_size()
    _sum = sum([_dir.size for _dir in fs.dirs if _dir.size < PART_1])
    logger.info(f"Part 1: Sum of dirs smaller than {PART_1} Bytes: {_sum} Bytes")
    # fs.print_fs()
    _size_deleted_dir = fs.delete_dir_for_update(update_size=PART_2)
    # fs.print_fs()
    logger.info(f"Part 2: Dir deleted with size: {_size_deleted_dir} bytes")

if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))
