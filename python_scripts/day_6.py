import sys
from time import time
day = sys.argv[0].split("/")[-1].split("_")[1].removesuffix(".py")

class Item_Stack:
    """
    A stack data structure that can hold a maximum of items,
    depending on the value of the `amount_of_unique` parameter passed to the `__init__` method.
    """
    def __init__(self, amount_of_unique) -> None:
        """
        Initialize the stack and set the `total` and `amount_of_unique` attributes.
        
        Args:
            amount_of_unique (int): The part number for the stack.
        """
        self.stack = []
        self.total = 0
        self.amount_of_unique = amount_of_unique

    def push(self, item):
        """
        Add an `item` to the end of the stack. If the length of the stack is
        greater than `amount_of_unique`, the first item in the stack is removed
        to keep the stack at a maximum length of `amount_of_unique`.
        
        Args:
            item (any): The item to add to the stack.
        """
        self.stack.append(item)
        self.total += 1
        if len(self.stack) > self.amount_of_unique:
            self.stack.pop(0)

    def is_unique(self):
        """
        Check if the current items in the stack are unique.
        
        Returns:
            bool: `False` if the length of the stack is less than `amount_of_unique`,
            and `True` if the length of the stack is equal to `amount_of_unique`
            and all the items in the stack are unique.
        """
        if len(self.stack) < self.amount_of_unique:
            return False
        if len(set(self.stack)) == self.amount_of_unique:
            return True
    
    def __str__(self):
        """
        Return a string representation of the stack, which is the concatenation
        of the items in the stack.
        
        Returns:
            str: The string representation of the stack.
        """
        return "".join(self.stack)

def read_file(file_path):
    """
    Read the contents of a file.
    
    Args:
        file_path (str): The path to the file to read.
    
    Returns:
        str: The contents of the file.
    """
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def find_marker(puzzle_input, part):
    """
    Find the first occurrence of a unique sequence of characters in a string.
    
    Args:
        puzzle_input (str): The string to search for a unique sequence.
        part (int): The part number for the search.
    
    Returns:
        tuple: A tuple containing the part number, the `Item_Stack` instance
        containing the unique sequence, and the total number of characters processed
        before the unique sequence was found.
    """
    amount_of_unique = 4 if part == 1 else 14
    item_stack = Item_Stack(amount_of_unique)
    for _char in puzzle_input:
        item_stack.push(_char)
        if item_stack.is_unique():
            return part, item_stack, item_stack.total

def solve(puzzle_input):
    """
    Solve the puzzle by finding the first occurrence of a unique sequence of
    characters in the `puzzle_input` string for both part 1 and part 2 of the puzzle.
    
    Args:
        puzzle_input (str): The input string to solve the puzzle with.
    
    Returns:
        None
    """
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
