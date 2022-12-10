import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")
import re
from collections import defaultdict
from loguru import logger
# logger.remove()
logger.add("logging.log", level="INFO")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def cargos_into_stacks(cargo_lines):
    stacks = defaultdict(list)
    for cargo_line in cargo_lines:
        stack_no = 1
        if re.search(r"\d", cargo_line) is not None:
            break
        for cargo in range(1, len(cargo_line), 4):
            if cargo_line[cargo] != " ":
                stacks[stack_no].append(cargo_line[cargo])
            stack_no += 1
    stacks = {k: v[::-1] for k, v in stacks.items()}
    return stacks

def create_instructions(text_lines):
    # move 1 from 2 to 1
    instructions = []
    for line in text_lines:
        line_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
        match = line_regex.match(line)
        if match:
            instruction = {}
            instruction["move"] = int(match.group(1))
            instruction["from"] = int(match.group(2))
            instruction["to"] = int(match.group(3))
            instructions.append(instruction)
    return instructions

def part_1(stacks, instructions):
    for instruction in instructions:
        _from = instruction["from"]
        _to = instruction["to"]
        _amount = instruction["move"]
        for _ in range(_amount):
            stacks[_to].append(stacks[_from].pop())
    answer = ""
    for stack in range(1, len(stacks.keys())+1):
        answer += "".join(stacks[stack].pop())
    return answer

def part_2(stacks, instructions):
    for instruction in instructions:
        _from = instruction["from"]
        _to = instruction["to"]
        _amount = instruction["move"]
        stacks[_to] = stacks[_to] + stacks[_from][-_amount:]
        for _ in range(_amount):
            stacks[_from].pop()
    answer = ""
    for stack in range(1, len(stacks.keys())+1):
        answer += "".join(stacks[stack].pop())
    return answer

def solve(puzzle_input):
    logger.info(f"Solving puzzle day {day}...")
    text_lines = puzzle_input.splitlines()
    cargo_stacks = cargos_into_stacks(text_lines)
    instructions = create_instructions(text_lines)
    answer = part_1(cargo_stacks, instructions)
    logger.info(answer)
    cargo_stacks = cargos_into_stacks(text_lines)
    answer = part_2(cargo_stacks, instructions)
    logger.info(answer)
    
    
def main():
    solve(read_file(f"python_scripts/day_{day}.txt"))

if __name__ == '__main__':
    main()