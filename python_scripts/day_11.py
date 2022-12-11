import sys
from time import time
from loguru import logger
from aocd import get_data
import re
# logger.remove()
from math import lcm
logger.add("logging.log", level="INFO")
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

def read_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        return f.read()

class Monkey():
    mon_num = 0
    monkeys = []
    lcm_divider = 1
    part = 1
    def __init__(self, items, operator, operand, test_divider, action_true, action_false) -> None:
        self.name = f"Monkey {Monkey.mon_num}"
        self.mon_num = Monkey.mon_num
        Monkey.mon_num += 1
        self.items = items
        self.operator = operator
        self.operand = operand
        self.test_divider = test_divider
        self.action_true = action_true
        self.action_false = action_false
        
        self.inspected_items = 0
        
    def operate(self, item_idx):
        _operand = self.items[item_idx] if self.operand == "old" else int(self.operand)  
        if self.operator == "*":
            self.items[item_idx] *= _operand
        if self.operator == "/":
            self.items[item_idx] = int(self.items[item_idx] / _operand)
        if self.operator == "+":
            self.items[item_idx] += _operand
        if self.operator == "-":
            self.items[item_idx] -= _operand
    
    def divide(self, item_idx):
        if Monkey.part == 1:
            self.items[item_idx] = int(self.items[item_idx] / 3)
        else:
            self.items[item_idx] = self.items[item_idx] % Monkey.lcm_divider
    
    def test(self, item_idx):
        if Monkey.part == 1:
            return self.items[item_idx] % self.test_divider == 0
        if Monkey.part == 2:
            return self.items[item_idx] % self.test_divider == 0
        
    
    def next_monkey(self, item_idx):
        return self.action_true if self.test(item_idx) else self.action_false
    
    def __str__(self) -> str:
        return f"{self.name}: \n\tItems: {self.items}\n \
            \tOperator: {self.operator}\n \
            \tOperand: {self.operand}\n \
            \tTest divider: {self.test_divider}\n \
            \tAction true: {self.action_true}\n \
            \tAction false: {self.action_false}\n \
            \tInspected items: {self.inspected_items}"

    @classmethod
    def find_monkey(_class, idx):
        for monkey in _class.monkeys:
            if monkey.mon_num == idx:
                return monkey
            
    def throw(self, item_idx, to_monkey:int):
        next_monkey = Monkey.find_monkey(to_monkey)
        next_monkey.items.append(self.items[item_idx])
    
    def clear_items(self):
        self.inspected_items += len(self.items)
        self.items = []

    @classmethod
    def calculate_monkey_buisness(_class):
        # find 2 monkeys with most items
        mon_1 = max(_class.monkeys, key=lambda monkey: monkey.inspected_items)
        mon_2 = max(_class.monkeys, key=lambda monkey: monkey.inspected_items if monkey != mon_1 else 0)
        return mon_1.inspected_items * mon_2.inspected_items
        
def solve(puzzle_input, part, rounds):
    logger.info(f"Solving puzzle - day {day}...")
    Monkey.part = part
    Monkey.monkeys = []
    Monkey.mon_num = 0
    monkeys_input = puzzle_input.split("Monkey")
    for monkey_input in monkeys_input[1:]:
        # items: Starting items: 79, 98, ...
        items = re.findall(r"Starting items: (.*)", monkey_input)[0].split(", ")
        items = [int(item) for item in items]
        operation_tuple = re.findall(r"Operation: new = old (\*|\+|\/|\-) (\d+|old)", monkey_input)
        operator = operation_tuple[0][0]
        operand = operation_tuple[0][1]
        divider = int(re.findall(r"Test: divisible by (\d+)", monkey_input)[0])
        action_true = int(re.findall(r"If true: throw to monkey (\d+)", monkey_input)[0])
        action_false = int(re.findall(r"If false: throw to monkey (\d+)", monkey_input)[0])
        Monkey.monkeys.append(Monkey(items, operator, operand, divider, action_true, action_false))

    Monkey.lcm_divider = lcm(*[monkey.test_divider for monkey in Monkey.monkeys])
    round = 0
    while round < rounds:
        for current_monkey in Monkey.monkeys:
            for item_idx, item in enumerate(current_monkey.items):
                current_monkey.operate(item_idx)
                current_monkey.divide(item_idx)
                next_monkey = current_monkey.next_monkey(item_idx)
                current_monkey.throw(item_idx, next_monkey)
            current_monkey.clear_items()
        round += 1
    
    logger.info(f"Result {part}: {Monkey.calculate_monkey_buisness()}")
        
if __name__ == '__main__':
    # if getting data from aoc via api
    # solve(get_data(year=2022, day=int(day)))
    solve(read_file(f"python_scripts/day_{day}.txt"), part=1, rounds=20)
    solve(read_file(f"python_scripts/day_{day}.txt"), part=2, rounds=10_000)
