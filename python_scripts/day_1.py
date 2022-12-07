import sys
from time import time
from loguru import logger
logger.remove()
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def solve(puzzle_input, top_n=3):
    
    elves = puzzle_input.strip().split('\n\n')
    elves = [elf.split('\n') for elf in elves]
    cal_per_elf = {}
    for elf_num, elf_cals in enumerate(elves):
        elf_name = f"elf_{elf_num}"
        cal_per_elf[elf_name] = 0
        for cal in elf_cals:
            cal_per_elf[elf_name] += int(cal)
    # sort dict by value
    sorted_cal_per_elf = sorted(cal_per_elf.items(), key=lambda x: x[1], reverse=True)
    _sum = 0
    for i in range(top_n):
        _sum += sorted_cal_per_elf[i][1]
    logger.info(f"DAY {day} - TOP {top_n} CALORIES")
    logger.info(f"1. {sorted_cal_per_elf[0][0]} with {sorted_cal_per_elf[0][1]} calories!")
    logger.info(f"2. {sorted_cal_per_elf[1][0]} with {sorted_cal_per_elf[1][1]} calories!")
    logger.info(f"3. {sorted_cal_per_elf[2][0]} with {sorted_cal_per_elf[2][1]} calories!")
    logger.info(f"Sum of them: {_sum}")

if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))