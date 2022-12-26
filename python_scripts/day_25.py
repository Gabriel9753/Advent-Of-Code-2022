import sys
import re
from time import time
from loguru import logger
from aocd import get_data
# logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

SNAFUS = []
snafu_dict = {"2": 2, "1": 1, "0": 0, "=": -2, "-": -1}

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def snafu_to_dec(snafu):
    dec = 0
    for i, value in enumerate(reversed(snafu)):
        dec += snafu_dict[value] * (5 ** i)
    return dec

def dec_to_snafu(dec):
    snafu = []
    while dec > 0:
        v, r = divmod(dec, 5)
        match r:
            case 0|1|2:
                snafu.append(str(r))
                dec = v
            case 3:
                snafu.append("=")
                dec = v + 1
            case 4:
                snafu.append("-")
                dec = v + 1
    return "".join(reversed(snafu))

def solve(puzzle_input):
    logger.info(f"Solving puzzle - day {day}...")
    logger.info("puzzle_input:", puzzle_input)
    for line in puzzle_input.splitlines():
        SNAFUS.append(re.findall(r"\d|=|-", line))
    # print(SNAFUS)
    _sum = 0
    for snafu in SNAFUS:
        _sum += snafu_to_dec(snafu)
    print(_sum)
    print(f"Part 1: {dec_to_snafu(_sum)}")

if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"))
