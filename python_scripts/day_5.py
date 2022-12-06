import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")
import regex as re

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def cargos_into_stacks(cargo_lines):
    cargo_stacks = []
    cargo_bottom_index = 0
    for i,text_line in enumerate(cargo_lines):
        if '1' in text_line:
            cargo_bottom_index = i-1
            break
    for _c in range(cargo_bottom_index, -1, -1):
        cargos = cargo_lines[_c].split(' ')
        ship_number = 1
        cargo_index = 0
        empty_cargo_ctr = 0
        while cargo_index < len(cargos):
            if cargos[cargo_index] != '':
                if cargo_bottom_index == _c:
                    cargo_stacks.append([cargos[cargo_index]])
                else:
                    cargo_stacks[ship_number-1].append(cargos[cargo_index])
                ship_number += 1
                empty_cargo_ctr = 0
            else:
                empty_cargo_ctr += 1
                if ship_number == 1 & empty_cargo_ctr >= 3:
                    ship_number += 1
                    empty_cargo_ctr = 0
                elif empty_cargo_ctr >= 4:
                    ship_number += 1
                    empty_cargo_ctr = 0
            cargo_index += 1
    return cargo_stacks

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

def solve(puzzle_input):
    print("Solving puzzle...")
    text_lines = puzzle_input.replace('[','').replace(']','').splitlines()
    cargo_stacks = cargos_into_stacks(text_lines)
    instructions = create_instructions(text_lines)
    
    for instruction in instructions:
        for _p in range(-instruction["move"], 0):
            cargo_stacks[instruction["to"]-1].append(cargo_stacks[instruction["from"]-1][_p])
        for _ in range(instruction["move"]):
            cargo_stacks[instruction["from"]-1].pop()
    answer = ""
    for stack in cargo_stacks:
        answer += "".join(stack.pop())
    print(answer)
    
    
def main():
    solve(read_file(f"python_scripts/day_{day}.txt"))

if __name__ == '__main__':
    start = time()
    main()
    print(f"Time elapsed: {time() - start} seconds")