import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def solve(puzzle_input):
    print("Solving puzzle...")
    print("puzzle_input:", puzzle_input)

if __name__ == '__main__':
    start = time()
    solve(read_file(f"python_scripts/day_{day}.txt"))
    print(f"Time elapsed: {time() - start} seconds")