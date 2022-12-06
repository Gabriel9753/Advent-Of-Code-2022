import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")


def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def solve(puzzle_input):
    print("Solving puzzle...")
    pairs = [pair.strip().split(",") for pair in puzzle_input.split("\n")]
    ctr_1 = 0
    ctr_2 = 0
    for pair in pairs:
        pair_part_1 = range(int(pair[0].split("-")[0]), int(pair[0].split("-")[1]) + 1)
        pair_part_2 = range(int(pair[1].split("-")[0]), int(pair[1].split("-")[1]) + 1)
        pair_part_1 = [str(i) for i in pair_part_1]
        pair_part_2 = [str(i) for i in pair_part_2]
        intersection = set(pair_part_1).intersection(set(pair_part_2))
        if intersection:
            ctr_2 += 1
        if intersection in [set(pair_part_1), set(pair_part_2)]:
            ctr_1 += 1
    print(f"1: {ctr_1}")
    print(f"2: {ctr_2}")

def main():
    solve(read_file(f"python_scripts/day_{day}.txt"))

if __name__ == '__main__':
    start = time()
    main()
    print(f"Time elapsed: {time() - start} seconds")
