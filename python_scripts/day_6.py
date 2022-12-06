import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

class Four_Item_Stack:
    def __init__(self, part) -> None:
        self.stack = []
        self.total = 0
        self.amount_of_unique = 4 if part == 1 else 14
    
    def push(self, item):
        self.stack.append(item)
        self.total += 1
        if len(self.stack) > self.amount_of_unique:
            self.stack.pop(0)
    
    def is_unique(self):
        if len(self.stack) < self.amount_of_unique:
            return False
        if len(set(self.stack)) == self.amount_of_unique:
            return True
    
    def __str__(self):
        return "".join(self.stack)

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def find_marker(puzzle_input, part):
    four_item_stack = Four_Item_Stack(part)
    for _char in puzzle_input:
        four_item_stack.push(_char)
        if four_item_stack.is_unique():
            return part, four_item_stack, four_item_stack.total

def solve(puzzle_input):
    print("Solving puzzle...")
    part, stack, nums = find_marker(puzzle_input, 1)
    print(f'Part {part}: {stack} (marker at position: {nums})')
    part, stack, nums = find_marker(puzzle_input, 2)
    print(f'Part {part}: {stack} (marker at position: {nums})')

def main():
    solve(read_file(f"python_scripts/day_{day}.txt"))

if __name__ == '__main__':
    start = time()
    main()
    print(f"Time elapsed: {time() - start} seconds")
