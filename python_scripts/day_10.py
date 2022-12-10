import sys
from time import time
from loguru import logger
from aocd import get_data
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

CRT_WIDTH = 40
CRT_HEIGHT = 6
CRT = [["🔘" for _ in range(CRT_WIDTH)] for _ in range(CRT_HEIGHT)]

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def calculate_signal_strength(register_x, clock):
    if clock in [20, 60, 100, 140, 180, 220]:
        return clock * register_x
    return 0

def draw_crt(register_x, clock):
    render_pos = (clock-1) % 40
    sprite_pos = [register_x-1, register_x, register_x+1]
    row = 0
    row = clock // 40
    for pos in sprite_pos:
        if render_pos == pos:
            CRT[row][pos] = "🍩"
    
def print_crt():
    for row in CRT:
        print("".join(row))

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    instructions = puzzle_input.splitlines()
    clock = 1
    register_x = 1
    signal_strength = 0
    print_crt()
    print("\n------------------------------------\n")
    for instruction in instructions:
        command = instruction.split(" ")[0]
        signal_strength += calculate_signal_strength(register_x, clock)
        draw_crt(register_x, clock)
        if command == "noop":
            clock += 1
        elif command == "addx":
            clock += 1
            signal_strength += calculate_signal_strength(register_x, clock)
            draw_crt(register_x, clock)
            register_x += int(instruction.split(" ")[1])
            clock += 1
    print_crt()
    logger.info(f"1. Signal_strength: {signal_strength}")

if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))
