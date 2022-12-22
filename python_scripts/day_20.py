import sys
from tqdm import tqdm
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines()]
    
def calculate(puzzle_input, multiplier, mixing_time):
    puzzle_input = [(i, int(e)*multiplier) for i, e in enumerate(puzzle_input)]
    order = puzzle_input.copy()
    _len = len(puzzle_input)-1
    for _ in tqdm(range(mixing_time)):
        for order_element in order:
            _index = puzzle_input.index(order_element)
            new_index = (_index + order_element[1]) % _len
            puzzle_input.insert(new_index, puzzle_input.pop(_index))
    index_zero = puzzle_input.index([x for x in puzzle_input if x[1] == 0][0])
    return sum([puzzle_input[(index_zero + (_r*1000)) % (len(puzzle_input))][1] for _r in range(1, 4)])
    

def solve(puzzle_input):
    print(f"Part 1: {calculate(puzzle_input, 1, 1)}")
    print(f"Part 2: {calculate(puzzle_input, multiplier=811589153, mixing_time=10)}")
    
if __name__ == '__main__':
    solve(read_file(f"python_scripts/day_{day}.txt"))
