import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def get_backpacks(line):
    # split the line in two with same length
    backpack_1, backpack_2 = line[:len(line)//2], line[len(line)//2:]
    return backpack_1, backpack_2

def get_value_for_char(_char):
    if _char.isupper():
        return ord(_char) - 64 + 26
    return ord(_char) - 96

def find_same_char_in_backpacks(backpack_1:str, backpack_2:str):
    for _char in backpack_1:
        if _char in backpack_2:
            return _char

def calc_prio(backpack_1, backpack_2):
    same_char = find_same_char_in_backpacks(backpack_1, backpack_2)
    prio = get_value_for_char(same_char)
    return prio

def find_char_for_all_backpacks(group):
    num_backpacks = len(group)
    for _char in group[0]:
        counter_other_backpacks = 0
        for backpack in group[1:]:
            if _char in backpack:
                counter_other_backpacks += 1
        if counter_other_backpacks == num_backpacks - 1:
            return _char

def solve(puzzle_input):
    print("Solving puzzle...")
    backpacks = puzzle_input.splitlines()
    # Part One
    priorities = []
    for backpack_line in backpacks:
        backpack_1, backpack_2 = get_backpacks(backpack_line)
        prio = calc_prio(backpack_1, backpack_2)
        priorities.append(prio)
    print(f"1. Priorities: {sum(priorities)}")

    # Part Two
    priorities = []
    backpack_groups = []
    for i, backpack_line in enumerate(backpacks):
        if i % 3 == 0:
            backpack_groups.append([backpack_line])
        else:
            backpack_groups[-1].append(backpack_line)
    for backpack_group in backpack_groups:
        prio = get_value_for_char(find_char_for_all_backpacks(backpack_group))
        priorities.append(prio)
    print(f"2. Priorities: {sum(priorities)}")

def main():
    solve(read_file(f"python_scripts/day_3.txt"))

if __name__ == '__main__':
    start = time()
    main()
    print(f"Time elapsed: {time() - start} seconds")
